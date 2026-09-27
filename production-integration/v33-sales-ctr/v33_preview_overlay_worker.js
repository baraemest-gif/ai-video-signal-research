const UPSTREAM = "https://57ec6ea9.ai-video-signal.pages.dev";

const CFG = {
  "/elevenlabs-cancellation-refund-policy/": {
    title: "ElevenLabs Refund Policy 2026: 14-Day Rule, Cancellation & Credits",
    description: "ElevenLabs refund policy 2026: see the 14-day unused-credit rule, how cancellation works, what happens to credits, and mobile/EU refund paths."
  },
  "/filmora-free-vs-paid/": {
    title: "Filmora Free vs Paid 2026: Watermark, Price & Is It Worth It?",
    description: "Filmora Free vs Paid 2026: compare watermark rules, export limits, AI credits, current pricing and when upgrading is actually worth it."
  },
  "/best-ai-video-tools-for-compliance-training/": {
    description: "Compare AI compliance video tools for policy/SOP training, SCORM/LMS delivery, completion tracking, localization, version updates and knowledge checks."
  },
  "/filmora-free-trial/": {
    description: "Filmora free trial guide for 2026: watermark rules, the current free-export reward, achievement trials, Creative Assets trial and when to upgrade."
  },
  "/ai-video-pricing-benchmarks/": {
    linkHtml: '<p class="internal-authority-link v33-sales-ctr">Before choosing from the benchmark, <a href="/best-ai-video-generators/">compare AI video generators by workflow and pricing</a> to match subscription cost with the job you actually need to do.</p>'
  },
  "/ai-video-annual-vs-monthly-pricing-comparison/": {
    linkHtml: '<p class="internal-authority-link v33-sales-ctr">If you have not settled on a provider yet, <a href="/best-ai-video-generators/">compare the leading AI video generators before choosing a billing term</a>; annual savings matter only after the workflow fit is proven.</p>'
  },
  "/ai-video-credits-usage-comparison/": {
    linkHtml: '<p class="internal-authority-link v33-sales-ctr">For the broader purchase decision, <a href="/best-ai-video-generators/">compare AI video generators by pricing model and workflow</a> before treating any vendor credit as equivalent value.</p>'
  }
};

async function proxy(request) {
  const u = new URL(request.url);
  const headers = new Headers(request.headers);
  headers.set("host", new URL(UPSTREAM).host);
  const init = { method: request.method, headers, redirect: "manual" };
  if (!["GET", "HEAD"].includes(request.method)) init.body = request.body;
  return fetch(UPSTREAM + u.pathname + u.search, init);
}

function previewHeaders(sourceHeaders, version) {
  const h = new Headers(sourceHeaders);
  h.delete("content-length");
  h.delete("content-encoding");
  h.delete("etag");
  h.set("cache-control", "no-store");
  h.set("x-robots-tag", "noindex, nofollow");
  h.set("x-aivs-v33-status", version);
  return h;
}

export default {
  async fetch(request) {
    const u = new URL(request.url);
    const cfg = CFG[u.pathname];
    const upstream = await proxy(request);

    if (!cfg || request.method !== "GET") return upstream;
    const ct = upstream.headers.get("content-type") || "";
    if (!ct.includes("text/html")) return upstream;

    if (cfg.linkHtml) {
      const original = await upstream.text();
      if (original.includes("v33-sales-ctr")) {
        return new Response(original, {
          status: upstream.status,
          headers: previewHeaders(upstream.headers, "patched-v5-existing")
        });
      }
      const re = /<\/h1\s*>/i;
      if (!re.test(original)) {
        const h = previewHeaders(upstream.headers, "guard-failed-v5");
        h.set("x-aivs-v33-reason", "missing-h1-close");
        return new Response(original, { status: upstream.status, headers: h });
      }
      const patched = original.replace(re, m => m + cfg.linkHtml);
      return new Response(patched, {
        status: upstream.status,
        headers: previewHeaders(upstream.headers, "patched-v5")
      });
    }

    let rw = new HTMLRewriter();
    if (cfg.title) {
      rw = rw
        .on("title", { element(el) { el.setInnerContent(cfg.title); } })
        .on('meta[property="og:title"]', { element(el) { el.setAttribute("content", cfg.title); } })
        .on('meta[name="twitter:title"]', { element(el) { el.setAttribute("content", cfg.title); } });
    }
    if (cfg.description) {
      rw = rw
        .on('meta[name="description"]', { element(el) { el.setAttribute("content", cfg.description); } })
        .on('meta[property="og:description"]', { element(el) { el.setAttribute("content", cfg.description); } })
        .on('meta[name="twitter:description"]', { element(el) { el.setAttribute("content", cfg.description); } });
    }

    const transformed = rw.transform(upstream);
    return new Response(transformed.body, {
      status: transformed.status,
      statusText: transformed.statusText,
      headers: previewHeaders(transformed.headers, "patched-v5")
    });
  }
};
