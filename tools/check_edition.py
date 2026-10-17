#!/usr/bin/env python3
"""Offline checks for a completed sharectl edition. Python 3.10+, stdlib only.

This checks markup and recorded evidence, not truth, permissions or live URLs.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

VOID = set("area base br col embed hr img input link meta param source track wbr".split())
KINDS = {"news", "background", "product", "video", "social", "editorial", "demo"}
DAILY = {"news", "video", "social"}
PLACEHOLDER = re.compile(r"\[[A-Z][A-Z_ ]*\]")


@dataclass
class Node:
    tag: str
    attrs: dict[str, str]
    line: int = 1
    parent: Node | None = None
    children: list = field(default_factory=list)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self):
        if self.tag in {"style", "script"}:
            return ""
        return " ".join(c.text() if isinstance(c, Node) else c for c in self.children).strip()

    def has_class(self, value):
        return value in self.attrs.get("class", "").split()


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node("document", {})
        self.stack = [self.root]
        self.fill_comments = []
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: v or "" for k, v in attrs}, self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def handle_comment(self, data):
        if "FILL" in data:
            self.fill_comments.append(self.getpos()[0])


def blocks(source, tag):
    return re.findall(rf"<{tag}\b[^>]*>.*?</{tag}\s*>", source, re.S | re.I)


def instant(value):
    if not isinstance(value, str):
        raise ValueError("expected an ISO timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp needs a verified UTC offset")
    return parsed


def canonical(url):
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid"}]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path or "/",
                       urlencode(sorted(query)), ""))


def http_url(value):
    if not isinstance(value, str):
        return False
    try:
        parts = urlsplit(value)
        return parts.scheme.lower() in {"http", "https"} and bool(parts.hostname) and not parts.username
    except (ValueError, TypeError):
        return False


def validate(source, *, template=None, manifest=None, as_of=None, max_age_hours=48,
             allow_demo=False, base_dir=None):
    """Return error/warning dictionaries; never fetch or execute source content."""
    result = []

    def issue(code, message, node=None, level="error"):
        result.append({"level": level, "code": code, "line": node.line if node else 1,
                       "message": message})

    now = instant(as_of) if isinstance(as_of, str) else as_of or datetime.now(timezone.utc)
    if now.tzinfo is None or not math.isfinite(max_age_hours) or max_age_hours <= 0:
        raise ValueError("as-of needs an offset and max-age-hours must be positive")
    doc = Document(source)
    nodes = list(doc.root.walk())
    ids = {}
    for node in nodes:
        ident = node.attrs.get("id")
        if ident:
            if ident in ids:
                issue("duplicate-id", f"Duplicate id: {ident}", node)
            ids[ident] = node
        if PLACEHOLDER.search(node.text()) and not any(PLACEHOLDER.search(c.text()) for c in node.children if isinstance(c, Node)):
            issue("placeholder", "Unfilled text placeholder", node)
        for name, value in node.attrs.items():
            value = value or ""
            if PLACEHOLDER.search(value) or "<!--" in value or "-->" in value:
                issue("placeholder", f"Unfilled/comment text in {name}", node)
            if name.lower().startswith("on") or name == "srcdoc":
                issue("unsafe-markup", f"Forbidden attribute: {name}", node)
            if "&amp;" in value:
                issue("double-escape", f"Possible double-escaped ampersand in {name}", node, "warning")
            urls = [value] if name in {"href", "src", "poster", "cite", "action"} else []
            if name == "style":
                urls += re.findall(r"url\(['\"]?(.*?)['\"]?\)", value, re.I)
                if re.search(r"expression\s*\(|@import", value, re.I):
                    issue("unsafe-markup", "Forbidden inline style expression/import", node)
            for url in urls:
                clean = re.sub(r"[\x00-\x20]", "", url)
                try:
                    scheme = urlsplit(clean).scheme.lower()
                except ValueError:
                    issue("unsafe-url", f"Malformed URL in {name}", node)
                    continue
                data_icon = node.tag == "link" and node.attrs.get("rel") == "icon" and clean.startswith("data:image/")
                if clean.startswith("//") or (scheme and scheme not in {"http", "https"} and not data_icon):
                    issue("unsafe-url", f"Disallowed URL in {name}", node)
                elif scheme in {"http", "https"} and not http_url(clean):
                    issue("unsafe-url", f"Invalid HTTP(S) URL in {name}", node)
                elif name in {"src", "poster"} and clean and not scheme and base_dir:
                    asset = Path(base_dir) / unquote(urlsplit(url).path)
                    if not asset.is_file():
                        issue("missing-asset", f"Missing local asset: {url}", node)
        if node.tag in {"base", "object", "embed", "form"} or (node.tag == "meta" and node.attrs.get("http-equiv", "").lower() == "refresh"):
            issue("unsafe-markup", f"Forbidden element: {node.tag}", node)
        if node.tag == "iframe":
            url = node.attrs.get("src", "")
            if not re.fullmatch(r"https://www\.youtube-nocookie\.com/embed/[\w-]{11}(?:\?[^\s]*)?", url):
                issue("unsafe-url", "Only the documented YouTube iframe is supported", node)
        if node.tag == "mark" and not any(p.tag == "blockquote" for p in ancestors(node)):
            issue("quote-placement", "Highlights belong inside a separate attributed quotation", node)

    def name(node):
        labelled = node.attrs.get("aria-labelledby", "").split()
        if labelled:
            return " ".join(ids[x].text() for x in labelled if x in ids)
        return node.attrs.get("aria-label", "").strip() or node.text() or " ".join(
            n.attrs.get("alt", "").strip() for n in node.walk() if n.tag == "img")

    for node in nodes:
        if node.tag in {"a", "button"} and not name(node):
            issue("accessible-name", f"{node.tag} has no accessible name", node)
        if node.tag == "img" and "alt" not in node.attrs:
            issue("image-alt", "Image needs alt (empty only when decorative)", node)
        if node.tag == "a" and node.attrs.get("href", "").startswith("#"):
            target = unquote(node.attrs["href"][1:])
            if target not in ids:
                issue("dead-anchor", f"Missing internal target: {target}", node)
        for target in node.attrs.get("aria-labelledby", "").split():
            if target not in ids:
                issue("dead-label", f"Missing aria-labelledby target: {target}", node)
    if sum(n.tag == "h1" for n in nodes) != 1:
        issue("h1", "Edition must have exactly one h1")
    if template is not None:
        for tag in ("style", "script"):
            if blocks(source, tag) != blocks(template, tag):
                issue("template-block", f"{tag} blocks differ from the supplied template")
    elif blocks(source, "script"):
        issue("untrusted-script", "Provide --template to verify script blocks")
    for tag in ("script", "style"):
        if sum(n.tag == tag for n in nodes) != len(blocks(source, tag)):
            issue("unsafe-markup", f"Unclosed or unsupported {tag} element")
    if any(n.tag == "link" and "stylesheet" in n.attrs.get("rel", "").split() for n in nodes):
        issue("template-block", "External stylesheets are not part of the inline template")
    if doc.fill_comments:
        issue("fill-comment", "Leftover FILL comments (not necessarily visible)", level="warning")

    demo = any(n.tag == "body" and n.attrs.get("data-demo") == "true" for n in nodes)
    if demo:
        if not allow_demo:
            issue("demo-mode", "Fictional demos require --allow-demo")
        if not any(n.attrs.get("data-demo-notice") == "true" and n.text() for n in nodes):
            issue("demo-label", "Fictional demo needs a visible data-demo-notice label")
        issue("demo-mode", "Fictional demo: no news freshness/evidence claims checked", level="warning")

    articles = [n for n in nodes if n.tag == "article"]
    if not articles:
        issue("no-stories", "Edition has no article cards")
    stories, primary_urls = {}, set()
    for article in articles:
        ident, kind = article.attrs.get("id", ""), article.attrs.get("data-kind", "")
        if kind not in KINDS:
            issue("story-kind", "Article needs a documented data-kind", article)
        prefix = "e-" if kind == "editorial" else "a-"
        if not re.fullmatch(prefix + r"[a-z0-9]+(?:-[a-z0-9]+)*", ident):
            issue("story-id", f"Article needs a unique stable {prefix}… id", article)
        if kind == "editorial":
            continue
        if kind == "demo" and not (demo and allow_demo):
            issue("demo-mode", "Demo cards require an explicitly allowed, labelled demo", article)
        heading = next((n for n in article.walk() if n.tag in {"h2", "h3"}), None)
        link = next((n for n in heading.walk() if n.tag == "a"), None) if heading else None
        url = link.attrs.get("href", "") if link else ""
        if not http_url(url):
            issue("original-link", "Story headline needs an HTTP(S) original link", article)
        else:
            normalized = canonical(url)
            if normalized in primary_urls:
                issue("duplicate-story", "Two story cards share the same original URL", article)
            primary_urls.add(normalized)
        card_nodes = list(article.walk())
        summary = next((n for n in card_nodes if n.has_class("dek") and n.text()), None)
        byline = next((n for n in card_nodes if n.has_class("by") and n.text()), None)
        if not summary:
            issue("summary", "Story needs its own visible summary", article)
        if not byline:
            issue("byline", "Story needs an author/publisher byline", article)
        if heading and summary and byline and not (card_nodes.index(heading) < card_nodes.index(summary) < card_nodes.index(byline)):
            issue("card-order", "Use headline, summary, optional content, then byline", article)
        published = article.attrs.get("data-published")
        if "data-published" not in article.attrs:
            issue("publication-date", "Article needs data-published (empty only for undated product guides)", article)
        stories[ident] = (article, published, url)
        if kind == "demo" and demo and allow_demo:
            continue
        if not published:
            if kind != "product":
                issue("publication-date", "Only labelled product guides may lack publication dates", article)
            else:
                issue("undated-product", "Check the visible missing-date/check-date labels manually", article, "warning")
            continue
        try:
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", published):
                date = datetime.strptime(published, "%Y-%m-%d").date()
                if kind in DAILY:
                    issue("publication-date", "Daily eligibility needs a verified time and offset", article)
                if date > now.date():
                    issue("future-date", "Publication date is in the future", article)
            else:
                when = instant(published)
                if when > now:
                    issue("future-date", "Publication time is in the future", article)
                elif kind in DAILY and now - when > timedelta(hours=max_age_hours):
                    issue("stale-news", "Daily story is outside the requested publication window", article)
        except ValueError as error:
            issue("publication-date", str(error), article)

    if manifest is not None:
        items = manifest.get("items") if isinstance(manifest, dict) else None
        if not isinstance(items, list) or not all(isinstance(x, dict) for x in items):
            issue("manifest", "Source record needs an items array of objects")
        else:
            seen, events = set(), set()
            for item in items:
                ident = item.get("id")
                if not isinstance(ident, str) or ident in seen or ident not in stories:
                    issue("manifest", f"Duplicate, invalid or unknown source-record id: {ident}")
                    continue
                seen.add(ident)
                article, published, url = stories[ident]
                if item.get("published_at") != (published or None):
                    issue("manifest-date", "Source record and card publication dates differ", article)
                if not http_url(item.get("url")) or not http_url(url) or canonical(item["url"]) != canonical(url):
                    issue("manifest-url", "Source record must match the primary original URL", article)
                if not http_url(item.get("source_url")):
                    issue("manifest-url", "Record the actual fetched HTTP(S) source URL", article)
                try:
                    fetched = instant(item.get("fetched_at"))
                    if fetched > now:
                        issue("manifest-fetch", "Fetch timestamp is in the future", article)
                    if published and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", published) and instant(published) > fetched:
                        issue("manifest-fetch", "Record was fetched before its claimed publication", article)
                except ValueError as error:
                    issue("manifest-fetch", str(error), article)
                event = item.get("event_id")
                if event is not None:
                    if not isinstance(event, str) or not event.strip():
                        issue("manifest-event", "event_id must be a non-empty string", article)
                    elif event in events:
                        issue("duplicate-event", f"Two cards describe the same recorded event: {event}", article)
                    else:
                        events.add(event)
            for ident in stories.keys() - seen:
                issue("missing-evidence", f"No source record for {ident}", stories[ident][0])
    return result


def ancestors(node):
    while node.parent:
        node = node.parent
        yield node


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edition", type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--as-of", help="ISO timestamp with offset; defaults to current UTC")
    parser.add_argument("--max-age-hours", type=float, default=48)
    parser.add_argument("--allow-demo", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        issues = validate(args.edition.read_text(encoding="utf-8"),
                          template=args.template.read_text(encoding="utf-8") if args.template else None,
                          manifest=json.loads(args.manifest.read_text(encoding="utf-8")) if args.manifest else None,
                          as_of=args.as_of, max_age_hours=args.max_age_hours,
                          allow_demo=args.allow_demo, base_dir=args.edition.parent)
    except (OSError, ValueError, UnicodeError) as error:
        issues = [{"level": "error", "code": "input", "line": 1, "message": str(error)}]
    ok = not any(i["level"] == "error" for i in issues)
    if args.json:
        print(json.dumps({"ok": ok, "issues": issues}, ensure_ascii=False, indent=2))
    else:
        for item in issues:
            print(f"{item['level']}: {args.edition}:{item['line']}: {item['code']}: {item['message']}")
        print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
