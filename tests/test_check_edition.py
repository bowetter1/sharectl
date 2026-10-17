import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.check_edition import Document, validate

ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-10-16T12:00:00+02:00"
CARD = '''<article id="a-story" data-kind="news" data-published="2026-10-16T08:00:00+02:00">
<a href="https://publisher.example/story"><img src="https://publisher.example/picture.jpg" alt="Robot in a lab"></a>
<h2><a href="https://publisher.example/story">A qualified headline</a></h2>
<p class="dek">The company describes a planned pilot, not a completed deployment.</p><div class="by">Publisher</div></article>'''
PAGE = '<!doctype html><html><head><title>Edition</title></head><body><h1>Edition</h1>' + CARD + '</body></html>'
MANIFEST = {"items": [{"id": "a-story", "url": "https://publisher.example/story",
                       "source_url": "https://publisher.example/feed", "published_at": "2026-10-16T08:00:00+02:00",
                       "fetched_at": "2026-10-16T10:00:00+02:00", "event_id": "event-1"}]}


class EditionChecks(unittest.TestCase):
    def codes(self, page=PAGE, **kwargs):
        return {i["code"] for i in validate(page, as_of=NOW, **kwargs) if i["level"] == "error"}

    def test_valid_edition_and_manifest(self):
        self.assertEqual(self.codes(manifest=MANIFEST), set())

    def test_visible_and_attribute_placeholders_but_not_comment_errors(self):
        for bad in (PAGE.replace('A qualified headline', '[HEADLINE]'),
                    PAGE.replace('alt="Robot in a lab"', 'alt="[IMAGE_ALT]"'),
                    PAGE.replace('<body>', '<body aria-label="<!-- FILL -->Label">')):
            with self.subTest(bad=bad): self.assertIn('placeholder', self.codes(bad))
        self.assertFalse(self.codes(PAGE.replace('<body>', '<body><!-- FILL: old comment -->')))

    def test_duplicate_ids_and_dead_targets(self):
        self.assertIn('duplicate-id', self.codes(PAGE.replace('</body>', CARD+'</body>')))
        self.assertIn('dead-anchor', self.codes(PAGE.replace('</body>', '<a href="#missing">Read</a></body>')))
        self.assertNotIn('dead-anchor', self.codes(PAGE.replace('</body>', '<a href="#a-story">Read</a></body>')))

    def test_accessible_image_link_and_labelledby(self):
        self.assertIn('accessible-name', self.codes(PAGE.replace('alt="Robot in a lab"', 'alt=""')))
        named = PAGE.replace('<h1>', '<h1 id="page-name">').replace('alt="Robot in a lab"', 'alt=""').replace('<a href=', '<a aria-labelledby="page-name" href=')
        self.assertNotIn('accessible-name', self.codes(named))
        self.assertIn('dead-label', self.codes(named.replace('aria-labelledby="page-name"', 'aria-labelledby="unknown"')))
        self.assertIn('image-alt', self.codes(PAGE.replace(' alt="Robot in a lab"', '')))

    def test_exactly_one_h1(self):
        self.assertIn('h1', self.codes(PAGE.replace('<h1>Edition</h1>', '')))
        self.assertIn('h1', self.codes(PAGE.replace('<h1>', '<h1>Extra</h1><h1>')))

    def test_reject_unsafe_source_markup(self):
        for url in ['javascript:alert(1)', 'java&#10;script:alert(1)', 'data:text/html,bad', '//evil.example/x', 'https://[bad']:
            with self.subTest(url=url):
                self.assertIn('unsafe-url', self.codes(PAGE.replace('https://publisher.example/story', url)))
        for markup in ['<img onerror="alert(1)" alt="x">', '<iframe srcdoc="bad"></iframe>',
                       '<base href="https://evil.example">', '<form action="https://evil.example"></form>',
                       '<iframe src="https://evil.example"></iframe>']:
            with self.subTest(markup=markup):
                self.assertTrue(self.codes(PAGE.replace('</body>', markup+'</body>')) & {'unsafe-markup', 'unsafe-url'})

    def test_missing_local_asset(self):
        with tempfile.TemporaryDirectory() as folder:
            page = PAGE.replace('https://publisher.example/picture.jpg', 'local.svg')
            self.assertIn('missing-asset', self.codes(page, base_dir=folder))
            Path(folder, 'local.svg').write_text('<svg/>')
            self.assertNotIn('missing-asset', self.codes(page, base_dir=folder))

    def test_original_publication_window_and_offsets(self):
        for date, code in [('2026-10-14T11:59:59+02:00', 'stale-news'),
                           ('2026-10-17T09:00:00+02:00', 'future-date'),
                           ('2026-10-16T08:00:00', 'publication-date'),
                           ('2026-10-16', 'publication-date'), ('bad', 'publication-date')]:
            with self.subTest(date=date):
                self.assertIn(code, self.codes(PAGE.replace('2026-10-16T08:00:00+02:00', date)))
        self.assertNotIn('stale-news', self.codes(PAGE.replace('2026-10-16T08:00:00+02:00', '2026-10-14T12:00:00+02:00')))
        self.assertFalse(self.codes(PAGE.replace('2026-10-16T08:00:00+02:00', '2026-10-16T06:00:00Z')))

    def test_old_event_date_does_not_age_new_article(self):
        manifest = copy.deepcopy(MANIFEST); manifest['items'][0]['event_date'] = '2024-01-01'
        self.assertFalse(self.codes(manifest=manifest))

    def test_video_and_social_use_upload_post_time(self):
        for kind in ['video', 'social']:
            with self.subTest(kind=kind):
                page = PAGE.replace('data-kind="news"', f'data-kind="{kind}"').replace('2026-10-16T08:00:00+02:00', '2024-01-01T08:00:00Z')
                self.assertIn('stale-news', self.codes(page))

    def test_dated_background_and_undated_product(self):
        background = PAGE.replace('data-kind="news"', 'data-kind="background"').replace('2026-10-16T08:00:00+02:00', '2024-01-01')
        self.assertFalse(self.codes(background))
        self.assertIn('future-date', self.codes(background.replace('2024-01-01', '2027-01-01')))
        product = PAGE.replace('data-kind="news"', 'data-kind="product"').replace('2026-10-16T08:00:00+02:00', '')
        self.assertFalse(self.codes(product))
        self.assertIn('publication-date', self.codes(product.replace(' data-published=""', '')))

    def test_duplicate_original_url_ignores_tracking(self):
        second = CARD.replace('a-story', 'a-second').replace('https://publisher.example/story', 'https://publisher.example/story?utm_source=feed#part')
        self.assertIn('duplicate-story', self.codes(PAGE.replace('</body>', second+'</body>')))
        different = second.replace('story?utm_source=feed#part', 'story?id=other')
        self.assertNotIn('duplicate-story', self.codes(PAGE.replace('</body>', different+'</body>')))

    def test_manifest_mismatches_and_invalid_types(self):
        for field, value, code in [('id', 'a-unknown', 'manifest'), ('url', 'https://publisher.example/other', 'manifest-url'),
                                   ('published_at', '2024-01-01', 'manifest-date'), ('source_url', None, 'manifest-url'),
                                   ('url', [], 'manifest-url'), ('url', {}, 'manifest-url'),
                                   ('source_url', 42, 'manifest-url'), ('source_url', False, 'manifest-url'),
                                   ('fetched_at', '2026-10-17T10:00:00Z', 'manifest-fetch'),
                                   ('fetched_at', '2026-10-15T10:00:00Z', 'manifest-fetch'),
                                   ('fetched_at', None, 'manifest-fetch'), ('event_id', [], 'manifest-event')]:
            manifest = copy.deepcopy(MANIFEST); manifest['items'][0][field] = value
            with self.subTest(field=field, value=value): self.assertIn(code, self.codes(manifest=manifest))
        for value in [[], {'items': None}, {'items': [None]}, {'items': [{'id': []}]}]:
            with self.subTest(value=value): self.assertIn('manifest', self.codes(manifest=value))
        self.assertIn('missing-evidence', self.codes(manifest={'items': []}))

    def test_manifest_duplicate_event(self):
        second = CARD.replace('a-story', 'a-second').replace('/story', '/other')
        page = PAGE.replace('</body>', second+'</body>')
        manifest = copy.deepcopy(MANIFEST)
        item = copy.deepcopy(manifest['items'][0]); item.update(id='a-second', url='https://publisher.example/other')
        manifest['items'].append(item)
        self.assertIn('duplicate-event', self.codes(page, manifest=manifest))

    def test_highlight_is_separate_from_translated_summary(self):
        bad = PAGE.replace('A qualified headline', '<mark>A qualified headline</mark>')
        self.assertIn('quote-placement', self.codes(bad))
        quote = '<blockquote cite="https://publisher.example/story"><p><mark>Short original quote.</mark></p><cite>Publisher</cite></blockquote>'
        self.assertNotIn('quote-placement', self.codes(PAGE.replace('</article>', quote+'</article>')))

    def test_css_and_scripts_must_match_template(self):
        page = PAGE.replace('</head>', '<style>body{color:black}</style></head>')
        self.assertFalse(self.codes(page, template=page))
        self.assertIn('template-block', self.codes(page.replace('color:black', 'color:red'), template=page))
        script = PAGE.replace('</body>', '<script>trusted()</script></body>')
        self.assertIn('untrusted-script', self.codes(script))
        self.assertFalse(self.codes(script, template=script))
        self.assertIn('template-block', self.codes(script.replace('trusted()', 'changed()'), template=script))
        self.assertIn('unsafe-markup', self.codes(PAGE + '<script src="https://evil.example/x.js"/>', template=PAGE))
        self.assertIn('template-block', self.codes(PAGE.replace('</head>', '<link rel="stylesheet" href="https://evil.example/x.css"></head>'), template=PAGE))

    def test_card_order_and_byline(self):
        self.assertIn('byline', self.codes(PAGE.replace('<div class="by">Publisher</div>', '')))
        byline = '<div class="by">Publisher</div>'
        bad = PAGE.replace(byline, '').replace('<h2>', byline+'<h2>')
        self.assertIn('card-order', self.codes(bad))

    def test_every_template_card_follows_the_contract(self):
        document = Document((ROOT/'template.html').read_text())
        cards = [n for n in document.root.walk() if n.tag == 'article']
        self.assertEqual(len(cards), 9)
        self.assertEqual(len({n.attrs['id'] for n in cards}), len(cards))
        for card in cards:
            with self.subTest(card=card.attrs['id']):
                self.assertTrue(card.attrs['id'].startswith('a-'))
                self.assertIn(card.attrs['data-kind'], ['news', 'video', 'social'])
                self.assertIn('data-published', card.attrs)
                nodes = list(card.walk())
                headline = next(n for n in nodes if n.tag in ['h2', 'h3'])
                summary = next(n for n in nodes if n.has_class('dek'))
                byline = next(n for n in nodes if n.has_class('by'))
                self.assertLess(nodes.index(headline), nodes.index(summary))
                self.assertLess(nodes.index(summary), nodes.index(byline))

    def test_demo_requires_opt_in_and_visible_notice(self):
        demo = PAGE.replace('<body>', '<body data-demo="true"><p data-demo-notice="true">Fictional demo</p>').replace('data-kind="news"', 'data-kind="demo"').replace('2026-10-16T08:00:00+02:00', '2030-01-01')
        self.assertIn('demo-mode', self.codes(demo))
        self.assertFalse(self.codes(demo, allow_demo=True))
        self.assertIn('demo-label', self.codes(demo.replace('data-demo-notice="true"', ''), allow_demo=True))
        self.assertIn('h1', self.codes(demo.replace('<h1>Edition</h1>', ''), allow_demo=True))

    def test_cli_bad_input_returns_json_error(self):
        proc = subprocess.run([sys.executable, str(ROOT/'tools/check_edition.py'), '/missing/sharectl.html', '--json'], text=True, capture_output=True)
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(json.loads(proc.stdout)['ok'])

    def test_real_fictional_examples_use_exact_template(self):
        template = (ROOT/'template.html').read_text()
        for filename in ['example.html', 'tech-ai-vc-edition.html']:
            path = ROOT/'examples'/filename
            with self.subTest(filename=filename):
                self.assertFalse(self.codes(path.read_text(), template=template, allow_demo=True, base_dir=path.parent))


if __name__ == '__main__':
    unittest.main()
