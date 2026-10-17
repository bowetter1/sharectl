# Optional offline edition checks

The instruction-and-template workflow has no runtime dependency. When Python 3.10+ is available, this optional checker uses only its standard library:

```sh
python3 tools/check_edition.py /absolute/path/to/edition/index.html --template template.html
python3 tools/check_edition.py /absolute/path/to/edition/index.html --template template.html \
  --manifest /absolute/private/path/sources.json --as-of 2026-10-16T12:00:00+02:00
```

Exit **0** means no detected errors; **1** means an error or invalid input. Warnings do not fail the command. Add `--json` for structured `ok` / `issues` output. Omit `--as-of` to use current UTC. Use `--max-age-hours` for a reader-agreed different publication window; never widen it just to silence an error.

## What it checks

- Unfilled uppercase placeholders in rendered text and attributes, including comments accidentally left inside attributes. A standalone FILL comment is a warning, not a claim of a visible placeholder.
- Unique IDs, internal fragment targets, referenced accessible labels, exactly one `h1`, image alt attributes and accessible names on links/buttons.
- Canonical story IDs, documented `data-kind`, original headline links, summaries and duplicate original URLs (ignoring common tracking parameters).
- Future publication dates, explicit offsets, daily original-publication/upload windows. Date-only background is allowed; date-only daily news requires a verified time/offset. Undated product guides warn for manual label inspection.
- Exact CSS and script blocks against the supplied template. Without a template, scripts are rejected. This is a narrow template-integrity check, **not a general HTML sanitizer**.
- Obvious unsafe URLs/markup, inline event handlers and unsupported embeds. Missing relative image/media assets are errors. It never downloads resources or follows external links.
- With the optional [private source record](articles.md#optional-private-source-record): matching IDs, URLs/publication fields, fetched timestamps, missing records and duplicate recorded event IDs.
- Highlights belong in separate quotation blocks. It cannot judge quotation permission, accuracy or length limits.

The parser is intentionally small. Passing does **not** prove valid HTML in all browsers, visible background labels, accurate facts, actual fetching, source rights, successful live image loading, playable media, or the freshness of an unrecorded supporting link. Still perform the manual checks in [checks.md](checks.md), including desktop/mobile rendering and the original evidence. A source record is a declaration to check, not proof of truth. The checker does not execute or sanitize publisher HTML for you; extract and escape plain text.

## Fictional examples and CI

Fictional demos use `body data-demo="true"`, a visible element with `data-demo-notice="true"`, and `data-kind="demo"` for invented stories. They must be explicitly enabled:

```sh
python3 tools/check_edition.py examples/example.html --template template.html --allow-demo
python3 tools/check_edition.py examples/tech-ai-vc-edition.html --template template.html --allow-demo
python3 -m unittest discover -s tests -v
```

Demo mode clearly warns that freshness/evidence claims are not checked. It does not disable structural, accessibility, duplicate-URL, URL-safety or CSS/script checks. Never mark real news as demo to bypass a date error. Editorial overview/question cards use `data-kind="editorial"` and unique `e-…` IDs; they link back to story IDs instead of duplicating source cards.

Repository CI runs the offline tests and both fictional examples on supported Python versions. It makes no external network requests, so temporary publisher blocks cannot fail CI. Live source availability and media playback remain separate dated observations.
