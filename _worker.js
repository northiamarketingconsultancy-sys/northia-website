const PRODUCES = ['text/html', 'text/markdown'];
const PERMANENT_REDIRECTS = new Map([
  ['/influencer-marketing-asian-communities.html', '/kol-influencer-marketing-asia.html'],
  ['/kol-marketing-asia.html', '/kol-influencer-marketing-asia.html']
]);

function parseAccept(header) {
  if (!header || !header.trim()) return [{ type: '*/*', q: 1, order: 0 }];
  return header.split(',').map((raw, order) => {
    const parts = raw.trim().split(';').map((s) => s.trim());
    const type = (parts.shift() || '').toLowerCase();
    let q = 1;
    for (const p of parts) {
      const m = /^q\s*=\s*(0(?:\.\d{0,3})?|1(?:\.0{0,3})?)$/i.exec(p);
      if (m) q = Number(m[1]);
    }
    return { type, q, order };
  }).filter((x) => x.type && Number.isFinite(x.q));
}

function matchFor(representation, ranges) {
  const [rType] = representation.split('/');
  const matches = ranges.map((range) => {
    let specificity = -1;
    if (range.type === representation) specificity = 2;
    else if (range.type === `${rType}/*`) specificity = 1;
    else if (range.type === '*/*') specificity = 0;
    return { ...range, specificity };
  }).filter((m) => m.specificity >= 0);
  if (!matches.length) return { q: 0, specificity: -1, order: Number.MAX_SAFE_INTEGER };
  const maxSpecificity = Math.max(...matches.map((m) => m.specificity));
  return matches.filter((m) => m.specificity === maxSpecificity)
    .sort((a, b) => b.q - a.q || a.order - b.order)[0];
}

export function negotiate(acceptHeader, produces = PRODUCES) {
  const ranges = parseAccept(acceptHeader);
  const explicit = !!acceptHeader && acceptHeader.trim() !== '' && acceptHeader.trim() !== '*/*';
  const candidates = produces.map((mediaType, index) => ({ mediaType, index, ...matchFor(mediaType, ranges) }))
    .filter((x) => x.q > 0);
  if (!candidates.length) return null;
  candidates.sort((a, b) => b.q - a.q || (explicit ? a.order - b.order : a.index - b.index) || b.specificity - a.specificity);
  return candidates[0].mediaType;
}

function appendVary(headers, ...tokens) {
  const existing = (headers.get('Vary') || '').split(',').map((s) => s.trim()).filter(Boolean);
  const lower = new Set(existing.map((s) => s.toLowerCase()));
  for (const token of tokens) if (!lower.has(token.toLowerCase())) existing.push(token);
  headers.set('Vary', existing.join(', '));
}

function isDocumentPath(pathname) {
  return pathname === '/' || pathname.endsWith('/') || pathname.endsWith('.html');
}

function markdownPath(pathname) {
  if (pathname === '/') return '/index.md';
  if (pathname.endsWith('/')) return `${pathname}index.md`;
  return pathname.replace(/\.html$/, '.md');
}

function withHeaders(response, extra = {}) {
  const headers = new Headers(response.headers);
  appendVary(headers, 'Accept', 'Accept-Encoding');
  for (const [key, value] of Object.entries(extra)) headers.set(key, value);
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
}

async function assetFetch(env, request, pathname = null) {
  if (!pathname) return env.ASSETS.fetch(request);
  const url = new URL(request.url);
  url.pathname = pathname;
  return env.ASSETS.fetch(new Request(url.toString(), request));
}

function markdown404() {
  return '# 404 — Page not found\n\nThis URL does not exist on Northia Marketing Consultancy Ltd.\n\n## Where to look next\n\n- [Homepage](https://northiamarketing.com/)\n- [Agent guide](https://northiamarketing.com/llms.txt)\n- [Sitemap](https://northiamarketing.com/sitemap.xml)\n- [Asia market entry](https://northiamarketing.com/asia-market-entry-marketing.html)\n- [Community marketing](https://northiamarketing.com/community-marketing-services.html)\n';
}

export default {
  async fetch(request, env) {
    if (!['GET', 'HEAD'].includes(request.method)) return env.ASSETS.fetch(request);
    const url = new URL(request.url);
    const redirectPath = PERMANENT_REDIRECTS.get(url.pathname);
    if (redirectPath) return Response.redirect(new URL(redirectPath, url), 301);
    const asset = await assetFetch(env, request);

    if (asset.status === 404) {
      const choice = negotiate(request.headers.get('Accept'));
      if (choice === 'text/markdown') {
        const body = request.method === 'HEAD' ? null : markdown404();
        const headers = new Headers({ 'Content-Type': 'text/markdown; charset=utf-8' });
        appendVary(headers, 'Accept', 'Accept-Encoding');
        return new Response(body, { status: 404, headers });
      }
      return withHeaders(asset);
    }

    if (!isDocumentPath(url.pathname)) return asset;

    const choice = negotiate(request.headers.get('Accept'));
    if (!choice) {
      const headers = new Headers({ 'Content-Type': 'text/plain; charset=utf-8' });
      appendVary(headers, 'Accept', 'Accept-Encoding');
      return new Response(request.method === 'HEAD' ? null : 'Not Acceptable\n', { status: 406, headers });
    }

    const mdPath = markdownPath(url.pathname);
    if (choice === 'text/markdown') {
      const md = await assetFetch(env, request, mdPath);
      if (md.ok) return withHeaders(md, { 'Content-Type': 'text/markdown; charset=utf-8', 'Link': `</llms.txt>; rel="describedby"` });
      const htmlAllowed = negotiate(request.headers.get('Accept'), ['text/html']);
      if (!htmlAllowed) {
        const headers = new Headers({ 'Content-Type': 'text/plain; charset=utf-8' });
        appendVary(headers, 'Accept', 'Accept-Encoding');
        return new Response(request.method === 'HEAD' ? null : 'Not Acceptable\nMarkdown representation is not available and HTML is not acceptable.\n', { status: 406, headers });
      }
    }

    return withHeaders(asset, {
      'Content-Type': 'text/html; charset=utf-8',
      'Link': `<${mdPath}>; rel="alternate"; type="text/markdown", </llms.txt>; rel="describedby"`
    });
  }
};
