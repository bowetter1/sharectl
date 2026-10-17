# Editor layer (Redaktionen)

The **editor layer** is an **optional** feature that adds editorial context, fact-checks, story ratings, and connections between stories. It is **not** enabled by default. Use it only when the reader explicitly requests editorial commentary or analysis.

## When to use the editor layer

**Use when:**
- Reader asks for "analysis", "context", "editorial view", or "what's really going on"
- Reader wants ratings/priorities ("what should I read first?")
- Reader wants fact-checking or source evaluation
- Reader asks to connect related stories

**Do NOT use when:**
- Reader wants just the news (default sharectl behavior)
- Reader asks to "remove commentary" or "just facts"
- Publishing a reader's private edition or notes in the repository. Public/shared editions need explicit reader authorization, permitted source use and removal of private data; editorial commentary does not waive those requirements. Repository demonstrations must be fictional.

## Core principles

### 1. Editor text is clearly separated from source text

Editor content appears in **distinct visual blocks** (pale yellow `.red` boxes) that are:
- Collapsed by default (reader must click to open)
- Clearly labeled "Redaktionen" / "Editor" / "Éditorial" (localized)
- Never mixed inline with article summaries. Optional `<mark>` highlights belong inside a separate attributed quotation, not the editor's translated summary.

### 2. Grounded only in fetched sources

**Every** editor note, fact-check, and connection must be grounded in sources **fetched in this run**. Never:
- Invent facts, numbers, or quotes
- Add context from memory or general knowledge
- Claim sources say something they don't
- Compare to data not in the fetched sources

### 3. Fact-checks state exact discrepancies

When fact-checking, **specify exactly** what's wrong:

**Good:**
- "Enkelkälla: Bloomberg, återgiven av TechNode. Avtalet är inte klart och volymen hemlig."
- "Bygger på en anonym källa ('an insider told Axios'), och FTC svarade inte på Ars fråga."
- "Analys, inte nyhet. Efterklokhet är en genre, och den här är välskriven."

**Bad:**
- "Källa osäker" (what's uncertain?)
- "Kan vara fel" (specify what could be wrong)
- "Verkar tveksamt" (state the actual issue)

When sources **agree**, say so. When sources **disagree**, state both positions. When information is **missing**, note what's absent.

### 4. Voice: optional dry wit and irony

**Default voice** (when reader hasn't specified): Seasoned, well-read editor with dry wit and irony. Think *The Economist* meets *Private Eye*.

**Targets:**
- Hype, spin, and press releases disguised as news
- Vague valuations and "people familiar with the matter"
- Marketing language ("revolutionary", "game-changing")
- Empty announcements ("exploring options", "in talks")

**Never target:**
- Individuals' private traits (appearance, personal life)
- Protected characteristics (race, gender, disability, etc.)
- Genuine hardship or misfortune
- Small companies or individuals with no PR apparatus

**Tone examples:**

✅ Good:
- "Självbetyg är den mest pålitliga betygsskalan – för den som sätter dem."
- "Den som trodde att exportkontroller var en amerikansk specialitet får uppdatera sin världsbild – i utkastform, förstås."
- "'Advanced talks' är som bekant ett tillstånd som kan pågå i åretal."

❌ Bad (too mean, personal, or altering facts):
- "CEO är inkompetent" (personal attack)
- "Företaget ljuger" (unless proven and stated in sources)
- Making up numbers or "correcting" figures not actually wrong

**Plain voice:** When reader asks for "no commentary", "just facts", or "plain": omit all jokes, keep only factual checks and connections.

### 5. One quip per editor note

Wit is a spice, not the meal. **One** well-placed quip per editor note, then move to facts and connections. The note can be serious; not every story needs a joke.

## Editor layer components

### (a) Ledare (always open)

A top section with 3 key stories the reader needs to know today, with editorial summaries. Always open (not collapsible). Links to story anchors in the edition.

**Structure:**
```html
<section class="avd red-sec" id="s-ledare" style="--s:#1d1d1f">
  <header class="w a-head">
    <h2>Ledare: [EDITORIAL TITLE]</h2>
    <p>Redaktionen · Tre saker du behöver veta idag</p>
  </header>
  <div class="w notiser">
    <article class="it notis" id="e-overview-one" data-kind="editorial">
      <div class="n-text">
        <p class="vinjett">Redaktionen</p>
        <h3 class="rub liten"><a href="#a-story-id">1. [HEADLINE]</a></h3>
        <p class="dek">[EDITORIAL SUMMARY WITH CONTEXT]</p>
      </div>
    </article>
    <!-- Repeat for items 2 and 3 -->
  </div>
</section>
```

### (b) Per-story editor note (collapsible)

Added after the summary and any optional quotation/permission-gated expansion, before `.by`, in every card variant. A `.more` link is optional and is never a placement requirement. The canonical order and story-ID rules are in [articles.md](articles.md). Collapsed by default.

**Structure:**
```html
<details class="red-d">
  <summary class="red-sum">
    <span class="red-lbl">Redaktionen <span class="betyg b-maste">Måste läsas · kaffet får vänta</span></span>
  </summary>
  <div class="red">
    <p><b>Varför det spelar roll:</b> [WHY IT MATTERS]</p>
    <p class="red-fakta"><b>Faktakoll:</b> [FACT CHECK]</p>
    <p class="red-hang"><b>Hänger ihop med:</b> <a href="#id">related story</a> · <a href="#id">another</a></p>
  </div>
</details>
```

**Rating badges:**
- `.b-maste` (Måste läsas / Must read / À lire absolument) — red, important
- `.b-skumma` (Skumma / Skim / Parcourir) — grey, can wait
- `.b-bakgrund` (Bakgrund / Background / Contexte) — blue, for deep dives
- `.b-press` (Pressmeddelande i kostym / Press release in disguise / Communiqué déguisé) — purple, marketing

Localize all labels to reader's language.

**What to include:**
- **Varför det spelar roll** (Why it matters): 1-2 sentences connecting to larger trends or implications
- **Faktakoll** (Fact check): Source evaluation, single-source warnings, missing confirmations, clarifications
- **Hänger ihop med** (Connects to): In-page anchor links (`#id`) to related stories in this edition

Omit sections with nothing to say. An editor note can have just fact-checking, or just connections.

### (c) Highlight key sentence

Optionally use `<mark class="red-mark">` to highlight a short original sentence **inside a separate attributed quotation**. The headline and `.dek` remain the agent's summary in the reader's language. No quotation or highlight is required when an appropriate permitted excerpt is unavailable.

**Rules:**
- Copy the short quoted source wording **verbatim** and attribute it with an original link; respect source terms and the agent's quotation limits.
- Highlight at most **one** short sentence per story. Localize accessible labels such as `title`.
- Never wrap a translated/paraphrased summary in `<mark>` and describe it as an original quote. If a quotation is translated, label the translation and omit the verbatim-original highlight.
- Place the mark in the quotation's `<p>` inside `<blockquote>`, outside `.dek`. See the [quote snippet](articles.md#optional-quotation-and-expansion).

### (d) Strikethrough for corrections

Use `<del>` **only** when a source actually updated or corrected a figure. **Never** for:
- Emphasis
- Opinion ("I think this is wrong")
- Speculation ("probably not accurate")

**Example:**
```html
<p class="dek">Revenue hit <del>$16.2 billion</del> $16.8 billion in Q3, according to updated figures.</p>
```

### (e) "Frågor att bevaka" section

A closing section with unanswered questions raised by the stories. Links back to the relevant articles.

**Structure:**
```html
<section class="avd red-sec" id="s-fragor" style="--s:#1d1d1f">
  <header class="w a-head">
    <h2>Frågor att bevaka</h2>
    <p>Redaktionen · Det som pressmeddelandena glömde att svara på</p>
  </header>
  <div class="w notiser">
    <article class="it notis" id="e-question-topic" data-kind="editorial">
      <div class="n-text">
        <p class="vinjett">Redaktionen</p>
        <h3 class="rub liten">[QUESTION AS HEADLINE]</h3>
        <p class="red-hang"><a href="#a-story-id">Till artikeln</a></p>
      </div>
    </article>
    <!-- Repeat for more questions -->
  </div>
</section>
```

## Verification checks

Before delivery, verify:

1. **All editor text has sources**: Every claim, number, and connection traces to fetched sources
2. **No altered numbers**: Facts and figures match the sources exactly
3. **All anchors resolve**: Every `<a href="#id">` link points to an actual story in this edition
4. **Labels localized**: "Redaktionen", ratings, section headers match reader's language
5. **Voice appropriate**: Quips target hype/spin, not individuals
6. **No overclaiming**: Editor notes don't assert more than sources support

## Examples

See `examples/tech-ai-vc-edition.html` for a **fictional** Tech/AI/VC layout demonstration with editor notes. Its companies, publishers, quotations and events are invented; it is not news evidence or a reader's personal edition. Both repository examples use the template's exact CSS and scripts. Demonstration quote/expansion text was written specifically for that example.
