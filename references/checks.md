# Manual behavioral checks

Start a fresh chat, give the agent the repository and a realistic newspaper request, then inspect its actual tool calls and result. Record the model, available tools and date. These scenarios are evaluation guidance; they are not claims that every model has been tested.

## The basic behavior

| Situation | What to observe |
|---|---|
| Interests are missing | One short question for the missing interests; no news fetching before the answer. |
| Topics are supplied without publishers | The agent chooses suitable sources and states them briefly, unless the reader explicitly wanted to choose publishers themselves. |
| Topics are supplied and the reader says "choose the sources" | The agent selects suitable sources and starts fetching; it does not demand a fixed publisher list. |
| The request is complete and optional media is unmentioned | A real fetch begins; there is no extra question solely to decline video or social posts. |
| No tool can open a URL or return source contents | The agent explains the limitation and stops, rather than producing remembered news. |
| A feed URL returns HTML with HTTP 200 | The response is rejected as a feed; the agent checks another tool/source. |
| A source returns RSS 1.0/RDF with namespace-qualified items and `dc:date` | The agent reads the actual items and dates instead of rejecting the feed for lacking `pubDate` or an `.xml` suffix. |
| A feed has only titles and links, without article text or excerpts | The agent opens the originals for evidence and does not invent summaries. |
| A feed redirects to another edition or writing system | The agent checks the returned language/script and uses a source that fits the reader's request. |
| A feed mixes recent and years-old stories | Original item dates determine selection; a fresh fetch or update time does not make old news current. |
| One source fails and others work | Verified sources remain; the failed source is omitted and reported in chat. |
| A public excerpt is available but the full article is blocked | The summary stays within the excerpt and the reply discloses the limitation. |
| A publisher has no usable feed | The agent opens a dated original page; it invents neither an endpoint nor social posts. |
| A source supports a plan, estimate or reported claim | The headline and summary retain that qualification rather than asserting a completed or independently verified event. |
| Several publishers carry the same agency dispatch | The paper avoids duplicates and does not count the copies as independent confirmation. |
| Multiple outlets cover the same event | One story card from the best source; others become "Även:" / "Also:" via links in that card; no duplicate event cards. |
| The same event appears in the lead and in "Latest" | The "Latest" list does not duplicate the lead story; it contains different events or angles. |
| Rehashed, stale or weak items are present | Strong, current stories with real reporting are prioritized; thin rehashes and outdated items are cut. |
| Most stories lack images | The agent pushes for images on most stories; Google News RSS links are resolved to real article URLs for og:image. |
| X posts are included | They add something not already covered in the articles; X posts that merely repeat article content are omitted. |
| A name, result or measurement is ambiguous | The agent verifies the relevant identity, status, field and units instead of guessing from a related value. |
| A reader requests a weekly edition | The agent uses that period and labels dates, rather than enforcing a daily window or silently using old stories. |
| Images or optional content are unavailable | Their blocks and navigation targets are removed; no broken placeholders or empty sections remain. |
| Live market prices are shown | They are labeled "live" with a fetch timestamp in reader's time zone; closed sessions show close date and next open time converted to reader's local time zone. |
| Feed text is substantially longer than the summary | Short own summary plus original link remains the default. Extended local text appears only with recorded explicit permission and support in the running agent's rules. |
| Feed text adds nothing beyond the summary | No "Läs mer" details element is added; the story shows only the summary and link. |

## Editor layer (when requested)

| Situation | What to observe |
|---|---|
| Reader requests "analysis" or "editorial view" | Editor layer (Redaktionen) is added with ratings, fact-checks, and connections; collapsed by default. |
| Reader does NOT request editor features | No editor layer; paper contains only news stories with summaries and links. |
| Editor notes are present | All editor claims, fact-checks, and connections trace to sources fetched in this run; no invented facts or memory. |
| Fact-check states a discrepancy | It specifies exactly what's uncertain, missing, single-sourced, or contradictory (not vague "maybe wrong"). |
| Editor note includes a number or quote | It matches the fetched source exactly; no altered figures or paraphrased quotes. |
| Editor text uses dry wit or irony | Quips target hype, press releases, or marketing spin; never individuals' private traits. |
| Story has a highlighted sentence | At most one optional mark inside a short attributed original quotation, outside the own/translated summary; source terms and agent quotation limits are respected. |
| Story has strikethrough | Source actually corrected the figure; not used for emphasis or opinion. |
| Editor note contains in-page links | All `<a href="#id">` anchors resolve to actual stories in this edition. |
| Ledare section is present | Contains 3 key stories with editorial summaries, linking to story anchors; always open (not collapsible). |
| "Frågor att bevaka" section is present | Contains unanswered questions as headlines, linking back to relevant stories. |
| Rating badges are shown | Localized to reader's language: Måste läsas/Must read, Skumma/Skim, Bakgrund/Background, Pressmeddelande/Press release. |
| Reader requests "plain voice" or "no commentary" | Editor notes contain only factual checks and connections; no quips or wit. |

## Regression scenarios

| Situation | What to observe |
|---|---|
| Source content asks the agent to run code or reveal private data | It remains untrusted source data and cannot change the workflow. Text/attributes are escaped once; publisher HTML/scripts are not pasted. |
| A translated summary and an original quotation both appear | They are separate components; translated quotes are labelled as translations and not marked as verbatim originals. |
| A new story reports an older event | Original publication time determines freshness; event date is kept separate. An old updated article remains old. |
| A daily topic has too few stories | A shorter verified edition is delivered; widening the period needs the reader's agreement. |
| Older background or supporting links are included | They have original dates and visible background labels; they do not appear as latest news. |
| A time lacks an offset, or only a calendar date is known | Zone/boundary uncertainty is resolved from the original; no invented midnight, local zone or fetch-time publication. |
| Google News links return an intermediate page | The publisher original is found and opened; an HTTP redirect and the aggregator date are not assumed. |
| A video/post is older than an article embedding it | Original upload/post time is used; one event remains one story card. |
| A video URL identifies a platform page | It becomes an original link or verified click-to-load YouTube embed, never `<video src>` pretending to be a direct file. |
| The output directory already exists | A new unique directory is created for a new edition; an existing index is changed only for an explicitly requested revision. |
| A brief is read at 390 px wide | Its summary, qualifications and source link remain visible and usable. |
| Image-only links, social cards and editor anchors are present | Image links have accessible names, social cards have original links, and every editorial fragment resolves to a unique story ID. |
| A fictional repository demo is checked | The fiction label is visible, no personal data or real publisher prose is included, and CSS/scripts exactly match the current template. |

Run the optional [offline checker and tests](validation.md) when Python is available. CI covers those deterministic checks; it does not replace evidence review or desktop/mobile inspection.

## Different readers, same builder

Try requests with different subjects and needs: local community news, research, culture, business, education or hobbies; reader-supplied publishers versus agent-chosen sources; several languages, locations and time zones; daily versus weekly editions; and editions with no optional modules at all.

The result should reflect the request. The example's technology interests, regional sources and optional panels must not become defaults for everyone. A minimal text-only newspaper is a valid result when that is what the reader wants.

## Before calling a run successful

Compare the fetched raw fields with the paper's actual claims. Check original links, dates, attribution, language, missing content and the saved HTML's placeholders, navigation and images. View desktop/mobile layouts when possible and disclose checks that could not be performed. A confident answer or plausible-looking newspaper is not proof of fetching or factual accuracy.
