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

ARTICLE_SLUGS = [
    'chinese-brands-north-america-market-entry-2026','asian-brands-overseas-localization-playbook-2026','asian-fb-brands-canada-market-entry-2026',
    'chinese-market-entry-marketing-2026','asia-market-entry-platform-strategy-2026','asian-consumer-market-entry-2026',
    'apac-influencer-marketing-benchmarks-2026','xiaohongshu-kol-marketing-2026','micro-influencer-community-strategy-2026',
    'community-marketing-strategy-2026','asian-community-marketing-north-america-2026','creator-to-community-funnel-2026',
    'chinese-restaurant-brands-north-america-2026','xiaohongshu-north-american-local-business-2026',
    'chinese-beauty-brands-canada-2026','xiaohongshu-account-strategy-north-america-2026'
]

def test_new_articles_are_agent_and_seo_ready():
    for slug in ARTICLE_SLUGS:
        html = (ROOT / f'{slug}.html').read_text(encoding='utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        assert len(soup.find_all('h1')) == 1
        assert len(' '.join(soup.stripped_strings)) > 500
        assert soup.find('meta', attrs={'name':'description'}).get('content')
        assert soup.find('link', attrs={'rel':'canonical'}).get('href').endswith(f'/{slug}.html')
        assert soup.find('script', attrs={'type':'application/ld+json'})
        assert soup.find('a', string=lambda x: x and 'Request a free audit' in x)
        people_label = soup.find('strong', string='People')
        assert people_label and people_label.find_next('span').get_text(strip=True)
        audience_section = soup.find('h2', string='People this guide is for')
        assert audience_section
        ld = json.loads(soup.find('script', attrs={'type':'application/ld+json'}).string)
        assert ld.get('audience', {}).get('audienceType')
        assert (ROOT / f'{slug}.md').exists()

def test_pillar_pages_have_guides_and_consultation_cta():
    for name in ['asia-to-world-marketing.html','asia-market-entry-marketing.html','kol-influencer-marketing-asia.html','community-marketing-services.html']:
        soup = BeautifulSoup((ROOT/name).read_text(encoding='utf-8'), 'html.parser')
        assert len(soup.select('.insight-card')) >= 3
        assert soup.select_one('.consult-band a[href="index.html#contact"]')

def test_new_guides_are_linked_from_requested_pages():
    slugs = ['chinese-restaurant-brands-north-america-2026.html','xiaohongshu-north-american-local-business-2026.html']
    for name in ['asia-to-world-marketing.html','asia-market-entry-marketing.html','mainland-china-market-entry-marketing.html']:
        soup = BeautifulSoup((ROOT/name).read_text(encoding='utf-8'), 'html.parser')
        hrefs = {a.get('href') for a in soup.find_all('a')}
        for slug in slugs:
            assert slug in hrefs

def test_latest_guides_have_complete_trilingual_sets():
    bases = ['chinese-restaurant-brands-north-america-2026','xiaohongshu-north-american-local-business-2026','chinese-beauty-brands-canada-2026','xiaohongshu-account-strategy-north-america-2026','influencer-vs-community-building-2026','ai-search-asian-brands-north-america-2026']
    variants = [('', 'en'), ('-zh-hk', 'zh-Hant'), ('-zh-cn', 'zh-Hans')]
    for base in bases:
        for suffix, lang in variants:
            html_path = ROOT/f'{base}{suffix}.html'
            md_path = ROOT/f'{base}{suffix}.md'
            assert html_path.exists() and md_path.exists()
            soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'html.parser')
            assert soup.html.get('lang') == lang
            assert len(soup.find_all('h1')) == 1
            assert soup.find('link', attrs={'rel':'canonical'}).get('href').endswith(f'/{base}{suffix}.html')
            hreflangs = {x.get('hreflang') for x in soup.find_all('link', attrs={'rel':'alternate'}) if x.get('hreflang')}
            assert {'en','zh-Hant','zh-Hans','x-default'} <= hreflangs

def test_localized_guides_are_linked_from_localized_requested_pages():
    for suffix in ['-zh-hk','-zh-cn']:
        slugs = [f'chinese-restaurant-brands-north-america-2026{suffix}.html', f'xiaohongshu-north-american-local-business-2026{suffix}.html']
        for base in ['asia-to-world-marketing','asia-market-entry-marketing','mainland-china-market-entry-marketing']:
            soup = BeautifulSoup((ROOT/f'{base}{suffix}.html').read_text(encoding='utf-8'), 'html.parser')
            hrefs = {a.get('href') for a in soup.find_all('a')}
            assert all(slug in hrefs for slug in slugs)

def test_september_2_guides_are_linked_from_all_requested_pages():
    for suffix in ['', '-zh-hk', '-zh-cn']:
        slugs = [f'chinese-beauty-brands-canada-2026{suffix}.html', f'xiaohongshu-account-strategy-north-america-2026{suffix}.html']
        for base in ['asia-to-world-marketing','asia-market-entry-marketing','mainland-china-market-entry-marketing']:
            soup = BeautifulSoup((ROOT/f'{base}{suffix}.html').read_text(encoding='utf-8'), 'html.parser')
            hrefs = {a.get('href') for a in soup.find_all('a')}
            assert all(slug in hrefs for slug in slugs)

def test_sitemap_and_llms_include_new_guides():
    sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
    llms=(ROOT/'llms.txt').read_text(encoding='utf-8')
    for slug in ARTICLE_SLUGS:
        assert f'https://northiamarketing.com/{slug}.html' in sitemap
        assert f'https://northiamarketing.com/{slug}.md' in llms
