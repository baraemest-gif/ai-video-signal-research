const TARGET_PATH = '/filmora-ai-credits/';
const MARKER = '<h2>Included AI credits by Filmora plan</h2>';
const PATCH_ID = 'aivs-filmora-free-vs-paid-link-v1';
const LIVE_HOST = 'aivideosignal.com';

const INSERT = `
<div data-aivs-overlay="${PATCH_ID}" class="decision-note" style="margin:1.25rem 0;padding:1rem 1.1rem;border:1px solid rgba(255,255,255,.14);border-radius:12px;">
  <strong>Still deciding whether you need a paid plan at all?</strong>
  Compare <a href="/filmora-free-vs-paid/">Filmora Free vs Paid</a> first, including the watermark, free-export exception and practical upgrade trigger.
</div>
`;

async function fetchUpstream(request, incoming) {
  if (incoming.hostname.endsWith('.workers.dev')) {
    const live = new URL(incoming.pathname + incoming.search, `https://${LIVE_HOST}`);
    return fetch(new Request(live, request));
  }
  return fetch(request);
}

export default {
  async fetch(request) {
    const incoming = new URL(request.url);
    const upstream = await fetchUpstream(request, incoming);

    if (request.method !== 'GET' || incoming.pathname !== TARGET_PATH) return upstream;

    const contentType = upstream.headers.get('content-type') || '';
    if (!contentType.toLowerCase().includes('text/html')) return upstream;

    const html = await upstream.text();
    const headers = new Headers(upstream.headers);
    headers.delete('content-length');
    headers.delete('content-encoding');

    if (html.includes(`data-aivs-overlay="${PATCH_ID}"`)) {
      headers.set('x-aivs-overlay', 'already-present');
      return new Response(html, { status: upstream.status, statusText: upstream.statusText, headers });
    }

    if (!html.includes(MARKER)) {
      headers.set('x-aivs-overlay', 'marker-not-found-noop');
      return new Response(html, { status: upstream.status, statusText: upstream.statusText, headers });
    }

    const patched = html.replace(MARKER, INSERT + MARKER);
    headers.set('x-aivs-overlay', PATCH_ID);
    return new Response(patched, { status: upstream.status, statusText: upstream.statusText, headers });
  }
};
