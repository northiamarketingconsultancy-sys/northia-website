import json
import re
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

class AgentReadinessStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / 'index.html').read_text(encoding='utf-8')
        cls.soup = BeautifulSoup(cls.html, 'html.parser')

    def test_homepage_is_meaningful_without_javascript(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        for tag in soup(['script', 'style']):
            tag.decompose()
        text = ' '.join(soup.stripped_strings)
        self.assertGreaterEqual(len(text), 500)
        self.assertEqual(len(soup.find_all('h1')), 1)
        self.assertGreaterEqual(len(soup.find_all('h2')), 3)
        self.assertNotIn('placeholder', text.lower())
        self.assertIn('From Asia, into new markets and communities.', text)
        self.assertIn('Northia Marketing Consultancy Ltd.', text)

    def test_agent_discovery_links_exist(self):
        alt = self.soup.find('link', attrs={'rel': lambda v: v and 'alternate' in v, 'type': 'text/markdown'})
        described = self.soup.find('link', attrs={'rel': lambda v: v and 'describedby' in v})
        self.assertEqual(alt.get('href'), '/index.md')
        self.assertEqual(described.get('href'), '/llms.txt')

    def test_llms_txt_has_required_shape_and_when_to_use_guidance(self):
        text = (ROOT / 'llms.txt').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('# Northia Marketing Consultancy Ltd.\n'))
        self.assertRegex(text, r'\n> .+\n')
        self.assertIn('Use Northia when', text)
        self.assertIn('## Core', text)
        links = re.findall(r'^- \[[^\]]+\]\(https://[^)]+\)', text, flags=re.M)
        self.assertGreaterEqual(len(links), 5)

    def test_404_has_recovery_links(self):
        text = (ROOT / '404.html').read_text(encoding='utf-8')
        self.assertIn('404 — Page not found', text)
        self.assertIn('llms.txt', text)
        self.assertIn('sitemap.xml', text)
        self.assertIn('noindex', text)

    def test_brand_structured_data_uses_exact_legal_name(self):
        ld = self.soup.find('script', attrs={'type': 'application/ld+json'})
        data = json.loads(ld.string)
        self.assertEqual(data['name'], 'Northia Marketing Consultancy Ltd.')
        self.assertEqual(data['legalName'], 'Northia Marketing Consultancy Ltd.')
        self.assertEqual(data['url'], 'https://northiamarketing.com/')
        self.assertIn('email', data)
        self.assertGreaterEqual(len(data.get('sameAs', [])), 2)

    def test_markdown_siblings_exist_for_html_content_pages(self):
        for html in ROOT.glob('*.html'):
            if html.name == '404.html':
                continue
            md = ROOT / ('index.md' if html.name == 'index.html' else f'{html.stem}.md')
            self.assertTrue(md.exists(), f'Missing markdown sibling for {html.name}')
            self.assertGreater(md.stat().st_size, 40, f'Markdown sibling is too small: {md.name}')

if __name__ == '__main__':
    unittest.main()


def test_homepage_search_snippet_is_brand_led():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "Northia — Asia ⇄ Overseas | Branding &amp; Community Consultancy" in html
    assert "Chinese market entry" in html
    assert "Asian community marketing in North America" in html
    assert '<div class="founders" data-nosnippet>' in html
