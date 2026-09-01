import test from 'node:test';
import assert from 'node:assert/strict';
import worker, { negotiate } from '../_worker.js';

test('legacy KOL aliases permanently redirect to the canonical page', async () => {
  const response = await worker.fetch(new Request('https://northiamarketing.com/kol-marketing-asia.html'), { ASSETS: { fetch: async () => new Response('unused') } });
  assert.equal(response.status, 301);
  assert.equal(response.headers.get('location'), 'https://northiamarketing.com/kol-influencer-marketing-asia.html');
});

const files = new Map([
  ['/', { body: '<!doctype html><h1>Home</h1>', type: 'text/html; charset=utf-8' }],
  ['/index.md', { body: '# Home\n\nAgent markdown.', type: 'text/markdown; charset=utf-8' }],
  ['/about.html', { body: '<h1>About</h1>', type: 'text/html; charset=utf-8' }],
  ['/about.md', { body: '# About', type: 'text/markdown; charset=utf-8' }],
]);

const env = {
  ASSETS: {
    async fetch(request) {
      const path = new URL(request.url).pathname;
      const hit = files.get(path);
      if (!hit) return new Response('<h1>404</h1>', { status: 404, headers: { 'Content-Type': 'text/html; charset=utf-8' } });
      return new Response(request.method === 'HEAD' ? null : hit.body, { status: 200, headers: { 'Content-Type': hit.type } });
    }
  }
};

function req(path='/', accept='text/html', method='GET') {
  return new Request(`https://northiamarketing.com${path}`, { method, headers: { Accept: accept } });
}

test('negotiation honors q values and explicit exclusions', () => {
  assert.equal(negotiate('text/markdown, text/html;q=0.8'), 'text/markdown');
  assert.equal(negotiate('text/markdown;q=0.2, text/html;q=0.9'), 'text/html');
  assert.equal(negotiate('text/html;q=0, */*;q=1'), 'text/markdown');
  assert.equal(negotiate('application/pdf'), null);
  assert.equal(negotiate(null), 'text/html');
});

test('canonical URL serves markdown with cache-safe Vary', async () => {
  const res = await worker.fetch(req('/', 'text/markdown'), env);
  assert.equal(res.status, 200);
  assert.match(res.headers.get('content-type'), /^text\/markdown; charset=utf-8/i);
  assert.match(res.headers.get('vary'), /Accept/i);
  assert.match(res.headers.get('vary'), /Accept-Encoding/i);
  assert.equal(await res.text(), '# Home\n\nAgent markdown.');
});

test('canonical URL serves HTML and advertises markdown + llms.txt', async () => {
  const res = await worker.fetch(req('/about.html', 'text/html'), env);
  assert.equal(res.status, 200);
  assert.match(res.headers.get('content-type'), /^text\/html; charset=utf-8/i);
  assert.match(res.headers.get('link'), /<\/about.md>; rel="alternate"; type="text\/markdown"/);
  assert.match(res.headers.get('link'), /<\/llms.txt>; rel="describedby"/);
});

test('unsupported document representation returns 406', async () => {
  const res = await worker.fetch(req('/', 'application/pdf'), env);
  assert.equal(res.status, 406);
  assert.match(res.headers.get('vary'), /Accept/i);
});

test('nonexistent paths return real 404 with markdown recovery when requested', async () => {
  const res = await worker.fetch(req('/does-not-exist', 'text/markdown'), env);
  assert.equal(res.status, 404);
  assert.match(res.headers.get('content-type'), /^text\/markdown/);
  const body = await res.text();
  assert.match(body, /# 404/);
  assert.match(body, /llms\.txt/);
  assert.match(body, /sitemap\.xml/);
});
