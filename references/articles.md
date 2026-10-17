# Article blocks and class glossary

Copy the supplied card variant from `template.html`; keep its classes, CSS and scripts. Change content, identifiers and optional components. The files in `examples/` are fictional visual demonstrations, never news sources.

## One content contract

Every story has a unique stable ID beginning `a-`, such as `a-origin-funding`, used by editorial links. Do not reuse the template's sample IDs when repeating a card. Set `data-kind` to `news`, `background`, `product`, `video` or `social`. Set `data-published` to its verified original ISO timestamp with offset, or a verified `YYYY-MM-DD` for dated background. An undated product guide has `data-published=""`, a visible missing-date/check-date label and belongs only in an agreed thematic edition. Daily news/video/social items need enough timestamp precision to establish their window eligibility.

Order every card as: optional image → linked headline → own summary → optional quotation/expansion → optional editor note → byline. A brief's thumbnail may be beside its text. Keep qualifications in visible text, including on mobile. A separate original link (`.more`) is optional because the headline already links to the publisher. Social and video cards also need visible original links.

```html
<article id="a-unique-story" class="it" data-kind="news"
         data-published="[VERIFIED_ISO_TIMESTAMP]" style="--c:#0b6bb3">
  <a class="bild" href="[ORIGINAL_URL]">
    <img src="[VERIFIED_IMAGE_URL]" alt="[MEANINGFUL_IMAGE_LINK_NAME]" loading="lazy">
  </a>
  <p class="vinjett">[LOCALIZED_CATEGORY]</p>
  <h3 class="rub mellan"><a href="[ORIGINAL_URL]">[OWN_HEADLINE]</a></h3>
  <p class="dek">[OWN_SUMMARY_WITH_QUALIFICATIONS]</p>
  <!-- Optional quotation/expansion, then editor note, go here. -->
  <div class="by"><span class="av" style="--c:#0b6bb3">[INITIALS]</span>
    <span><b>[VERIFIED_AUTHOR_OR_PUBLISHER]</b><small>[DATE_AND_VERIFIED_LOCAL_TIME]</small></span>
  </div>
</article>
```

Remove the entire image link if no permitted verified picture is available. Do not leave an empty `alt` on an image-only link: the image's meaningful alt provides its accessible name, or use a localized `aria-label` / valid `aria-labelledby` on the link. Escape text and attribute values **once**, after decoding entities from source data; `&amp;amp;` usually signals double escaping.

## Variants in the template

| Variant | Markup/classes | Use |
|---|---|---|
| Front-page lead | `.f-main > article.it.f-art`, `.rub.jatte` | One lead with a complete summary |
| Section lead | `.t-main > article.it.huvud-art`, `.rub.stor` | Section's main story |
| Sidebar | `.t-side > article.it.liten`, `.rub.liten` | Compact story, still with summary and byline |
| Column | `.tva > .spalt > article.it`, `.rub.mellan` | Equal-width article columns |
| Brief | `.notiser > article.it.notis > .n-text` | Short complete summary, thumbnail alongside |
| Social | `.r-grid > article.it.rost` | Own summary of a verified post and visible original link |
| Direct video | `article.tv-in` inside `.tv` | Verified permitted playable media file plus source link |
| YouTube | `.p-grid > article.p-art.mork` | Verified video ID, labelled play button, summary and watch link |

## Optional quotation and expansion

A quotation is separate from `.dek`. The original must have been fetched in this run and use must fit the source terms and the agent's quotation limits. An original-language quote can have **one optional** highlighted sentence; a translated quote is labelled as translated and has no verbatim-original highlight. All labels follow the reader's language.

```html
<blockquote cite="[ORIGINAL_URL]">
  <p><mark class="red-mark">[SHORT_VERBATIM_QUOTATION]</mark></p>
  <cite>[QUOTE_LABEL] · <a href="[ORIGINAL_URL]">[AUTHOR_OR_PUBLISHER]</a></cite>
</blockquote>
```

An expansion is **not required**. Only for explicitly permitted additional local text, record permission and scope privately and follow the [content policy](../SKILL.md#4-edit-for-this-reader). Never insert an article body merely because it is accessible. Public editions exclude extended full text. Omit this component when permission or useful additional text is absent.

```html
<details class="mer">
  <summary><span class="ls">[READ_MORE]</span><span class="vm">[SHOW_LESS]</span></summary>
  <div class="mer-box"><p>[PERMITTED_ADDITIONAL_PLAIN_TEXT]</p></div>
</details>
```

For editor notes use [editor.md](editor.md); insert them after optional content and before `.by`. Editorial overview/question cards use unique `e-…` IDs and `data-kind="editorial"`, linking to real `#a-…` stories. They do not create duplicate news cards.

## Optional private source record

The agent must retain evidence in its tool history or private notes. For machine checks, a small JSON record can accompany the edition **outside the public output**:

```json
{
  "items": [{
    "id": "a-unique-story",
    "url": "https://publisher.example/original",
    "source_url": "https://publisher.example/feed",
    "published_at": "2026-10-16T09:00:00+02:00",
    "event_date": "2026-10-14",
    "fetched_at": "2026-10-16T10:00:00+02:00",
    "event_id": "unique-event-key"
  }]
}
```

`published_at` must match the card; use `null` for undated product guides. `event_date` is optional and never replaces publication time. `event_id` is optional but lets the checker flag two cards for the same event even when URLs differ. `source_url` is the feed/API/page actually opened, and `url` is the card's primary original link. Permission notes, if needed, remain private. The checker validates recorded fields; it cannot prove they were fetched or are true. See [validation.md](validation.md).

## Class glossary

Names are retained for compatibility with the supplied design:

| Class | Meaning |
|---|---|
| `huvud`, `h-rad`, `h-namn` | Masthead, date row, newspaper title |
| `snav`, `pill` | Section navigation and its links |
| `w`, `avd`, `a-head` | Width wrapper, department, department heading |
| `forsta`, `f-main`, `f-side` | Front page, lead column, overview sidebar |
| `topp`, `t-main`, `t-side` | Section top, lead area, sidebar |
| `tva`, `spalt` | Two-column layout, column |
| `it`, `huvud-art`, `liten`, `notis` | Article, section lead, small article, brief |
| `bild`, `hel`, `tumme` | Image, contain/full image, thumbnail |
| `rub`, `jatte`, `stor`, `mellan`, `liten` | Headline and size variants |
| `vinjett`, `dek`, `by`, `av` | Kicker, summary, byline, initials/avatar badge |
| `mer`, `mer-box`, `red-d`, `red` | Permitted expansion and optional editor components |
| `mork`, `roster`, `citat` | Dark surface, social section, quotation styling |
