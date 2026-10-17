# International publisher examples

Read this reference when finding sources for a reader or checking a publisher-specific problem. It is a starting point across regions and languages, not a complete directory, ranking or default reading list. A local or specialist publication can fit the reader better than a large international brand.

**Checked 2026-10-16:** the feeds in the working tables returned parseable XML with dated entries inside a daily 48-hour window. These are access observations from one environment, not guarantees of continued availability, full-article access or permission to republish. Fetch and verify again for every edition. The links themselves lead to the publisher's feed; directories and access documentation are linked separately below.

## Choose the right edition

- Match the reader's sources, topics and source languages. A publisher's international, domestic and translated editions can carry different stories. Check the final URL after redirects and the actual language/script; do not infer them from a guessed path.
- Prefer an advertised topic, region or author feed when it fits better than the homepage feed. [Guardian feed guidance](https://www.theguardian.com/help/feeds) describes `/rss`; [Le Monde's directory](https://www.lemonde.fr/le-monde-et-vous/article/2025/07/14/les-flux-rss-du-monde-fr_5498778_3237.html), [SCMP's directory](https://www.scmp.com/feed-rss) and [AllAfrica's directory](https://allafrica.com/misc/tools/rss.html) offer more choices. Verify the chosen URL before using it.
- Separate the publisher, author and underlying reporting source. Several outlets carrying the same agency dispatch are not independent confirmations. AllAfrica also aggregates other publishers; retain the credited original source and follow its link when available.
- A title-only item can help discover an article but cannot support an invented summary. Open the article for more evidence, or omit it if the available material is insufficient.

## Content and permission

Follow the single [content policy in SKILL.md](../SKILL.md#4-edit-for-this-reader): short original summaries and publisher links are the default for both local and public editions. RSS availability is not a blanket reproduction license. Short quotations must be attributed and respect source terms and the agent's limits. A translation is not an original-language verbatim quotation.

An extended "Read more" panel is optional only when explicit rights-holder permission and the running agent's rules support the intended local use. Record the permission and scope privately. Never fetch article pages solely to reproduce their body, and omit extended full text from public/shared editions. Do not modify, translate or redistribute text when source terms prohibit it. Fictional repository examples contain no reader data or real publisher prose.

## Working feed examples

These feeds provided titles, original links and item dates. Most also provided excerpts; image and author fields vary. A feed excerpt does not establish access to the full article.

### International and North America

| Publication / edition | Source language | Feed and useful detail |
|---|---|---|
| BBC News | English | [News](https://feeds.bbci.co.uk/news/rss.xml); excerpts and thumbnails |
| BBC language editions | Spanish, Arabic, Hindi, Bengali, Indonesian | [Mundo](https://feeds.bbci.co.uk/mundo/rss.xml), [Arabic](https://feeds.bbci.co.uk/arabic/rss.xml), [Hindi](https://feeds.bbci.co.uk/hindi/rss.xml), [Bengali](https://feeds.bbci.co.uk/bengali/rss.xml), [Indonesian](https://feeds.bbci.co.uk/indonesia/rss.xml); choose the reader's source language |
| BBC Chinese | Traditional Chinese | [Chinese](https://feeds.bbci.co.uk/zhongwen/trad/rss.xml); the tested `/simp/` URL redirected to `/trad/`, so do not promise Simplified Chinese from that address |
| The Guardian | English | [World](https://www.theguardian.com/world/rss); dated items, excerpts and author fields |
| The New York Times | English | [Home page](https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml); excerpts, author and media fields; article access can differ |
| NPR | English | [News](https://feeds.npr.org/1001/rss.xml); excerpts and author fields |
| CBC | English | [Top stories](https://www.cbc.ca/webfeed/rss/rss-topstories); excerpts and author fields |
| The Wall Street Journal | English | [World](https://feeds.content.dowjones.io/public/rss/RSSWorldNews); excerpts, author and media fields; do not assume full-article access |
| Bloomberg | English | [Markets](https://feeds.bloomberg.com/markets/news.rss); redirects to Bloomberg's own domain; public excerpts |
| CNBC | English | [Top news](https://www.cnbc.com/id/100003114/device/rss/rss.html); XML despite the `.html` suffix; inspect the feed's item-type and sponsored labels when selecting stories |
| The Economist | English | [Latest](https://www.economist.com/latest/rss.xml); a large feed with older items too; filter individual publication dates |

### Europe

| Publication / edition | Source language | Feed and useful detail |
|---|---|---|
| Deutsche Welle | English, German | [English](https://rss.dw.com/rdf/rss-en-all), [German](https://rss.dw.com/rdf/rss-de-all); RSS 1.0/RDF, with `dc:date` rather than `pubDate` |
| France 24 | English, French | [English](https://www.france24.com/en/rss), [French](https://www.france24.com/fr/rss); excerpts, credits and media fields |
| Le Monde | French | [Headlines](https://www.lemonde.fr/rss/une.xml); public excerpts; topic feeds in its directory |
| EL PAÍS | Spanish | [Front page](https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada); excerpts, author and media fields |
| RTP | Portuguese | [News](https://www.rtp.pt/noticias/rss); excerpts and categories |
| ARD / tagesschau | German | [All reports](https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml); dates and excerpts |
| ANSA | Italian | [Headlines](https://www.ansa.it/sito/ansait_rss.xml); dated excerpts |
| NOS | Dutch | [General news](https://feeds.nos.nl/nosnieuwsalgemeen); excerpts and enclosures |
| Yle | Finnish | [Latest news](https://yle.fi/rss/uutiset/tuoreimmat); excerpts and categories |
| SVT | Swedish | [News](https://www.svt.se/nyheter/rss.xml); redirects to `/rss.xml` |

For the previously checked Financial Times, The Verge, Hacker News and Swedish newspaper examples, see [sources.md](sources.md). They use the same reader-led selection rules.

### Asia and the Middle East

| Publication / edition | Source language | Feed and useful detail |
|---|---|---|
| Al Jazeera | English, Arabic | [English](https://www.aljazeera.com/xml/rss/all.xml), [Arabic](https://www.aljazeera.net/aljazeerarss/ar/homepage); Arabic URL redirects; verify edition and dates |
| Asahi Shimbun | Japanese | [Headlines](https://www.asahi.com/rss/asahi/newsheadlines.rdf); RSS 1.0/RDF with `dc:date` and excerpts |
| Mainichi | Japanese | [Latest](https://mainichi.jp/rss/etc/mainichi-flash.rss); RSS 1.0/RDF with `dc:date`; sampled items had titles and links but no descriptions, so open articles before summarizing |
| Yonhap | Korean | [Latest](https://www.yna.co.kr/rss/news.xml); excerpts, author and media fields |
| CNA | English | [Latest](https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml); RSS XML despite `/api/` in the path; [feed terms](https://www.channelnewsasia.com/rss/rssterms) specify personal, non-commercial use |
| South China Morning Post | English | [News](https://www.scmp.com/rss/91/feed); excerpts, author and enclosures; use its directory for other subjects |

### Africa, Latin America and Oceania

| Publication / edition | Source language | Feed and useful detail |
|---|---|---|
| AllAfrica | English | [Latest](https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf); this `.rdf` URL returned RSS 2.0; retain the underlying publisher's credit |
| Africanews | English | [Latest](https://www.africanews.com/feed/rss); excerpts, authors and enclosures |
| Daily Maverick | English | [News](https://www.dailymaverick.co.za/dmrss/); excerpts, author and media fields |
| Folha de S.Paulo | Portuguese | [Latest](https://feeds.folha.uol.com.br/emcimadahora/rss091.xml); titles, dates, excerpts and authors |
| Globo / G1 | Portuguese | [G1](https://g1.globo.com/rss/g1/); excerpts and media fields; this working G1 feed does not establish that another Globo title has a feed |
| Clarín | Spanish | [Latest](https://www.clarin.com/rss/lo-ultimo/); excerpts, authors and enclosures |
| RNZ | English | [National](https://www.rnz.co.nz/rss/national.xml); dates include New Zealand's time-zone offset |

## Important exceptions found during the check

Use these observations to avoid common dead ends, not to exclude the publishers permanently.

| Source / tested address | Observation and next step |
|---|---|
| CNN — `http://rss.cnn.com/rss/edition.rss` | Returned XML with old items; the latest parsed item publication date was 2024-04-09. HTTPS also failed in this environment. Do not use the old feed for a current edition. Try dated original pages at [CNN](https://www.cnn.com/). |
| NHK — `https://www3.nhk.or.jp/rss/news/cat0.xml` | Returned August 2026 items outside the daily window; the tested old NHK World `/en/news/feeds/` address returned 404. Discover current links from [NHK](https://news.web.nhk/newsweb) or [NHK World](https://www3.nhk.or.jp/nhkworld/), then verify dates. |
| ABC Australia — [tested news feed](https://www.abc.net.au/news/feed/51120/rss.xml) | Returned current dated items, and a sampled original article confirmed its publication time. However, [ABC Help](https://help.abc.net.au/hc/en-us/articles/6147104938383-Why-are-RSS-feeds-no-longer-being-updated) says news RSS stopped being updated. Treat the feed as uncertain; recheck contents and originals rather than relying on either an old address or a help-page claim alone. |
| Washington Post | Its [feed directory](https://www.washingtonpost.com/information/2026/05/21/washington-post-rss-feeds/) lists feeds; the World feed returned 502 here. Retry an advertised feed or use accessible dated originals. |
| The Hindu; News24; O Globo; RTVE | The sampled addresses returned 403, a DNS error, non-XML and 404 respectively. No working feed was established in this check. Discover from the requested title's current official site; these failures do not prove the publisher has no feeds. |
| Times of India — [top stories](https://timesofindia.indiatimes.com/rssfeedstopstories.cms) | Returned current dated excerpts, but its [RSS terms](https://timesofindia.indiatimes.com/rss.cms) restrict modification, translation and redistribution. Do not treat successful fetching as blanket permission for a rewritten or published edition. |

## Existing APIs and AI access

Use these only when the reader already has suitable access and the host can call them. They are optional source routes, not services sharectl must implement or accounts the agent should create.

| Publisher | Documented access | What it means for the agent |
|---|---|---|
| Reuters | [Reuters MCP](https://reutersagency.com/reuters-mcp) | Reuters documents direct AI retrieval of text, photos and video with sourcing/rights metadata. Requires a Reuters content subscription and MCP credentials; documentation was checked, but authenticated retrieval was not tested. Prefer an existing authorized tool when available. |
| Associated Press | [AP Media API](https://developer.ap.org/ap-media-api/) | Licensed content access; requires an account/API key and the corresponding entitlements. Documentation was checked, not authenticated retrieval. Do not describe it as a free public RSS feed. |
| The Guardian | [Open Platform documentation](https://open-platform.theguardian.com/documentation/) | Requires an API key; supports content, tags, sections and editions with filters and rate limits. Public RSS remains a simpler option when sufficient. |
| BBC | [Information Syndication API](https://information-syndication.api.bbc.com/) | Requires a BBC syndication relationship and API key. It is separate from the public BBC feeds above. |

Keep credentials in the host's existing secure tools, never in this repository or the newspaper's HTML. Public access to excerpts or images is not a general republication license; retain original links and credits, and follow the selected source's usage terms.
