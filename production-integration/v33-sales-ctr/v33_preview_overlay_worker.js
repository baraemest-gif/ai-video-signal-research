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
  const upstreamUrl = UPSTREAM + u.pathname + u.search;
  const headers = new Headers(request.headers);
  headers.set("host", new URL(UPSTREAM).host);
  const init = { method: request.method, headers, redirect: "manual" };
  if (!["GET", "HEAD"].includes(request.method)) init.body = request.body;
  return fetch(upstreamUrl, init);
}

export default {
  async fetch(request) {
    const u = new URL(request.url);
    const cfg = CFG[u.pathname];
    const upstream = await proxy(request);

    if (!cfg || request.method !== "GET") return upstream;

    const contentType = upstream.headers.get("content-type") || "";
    if (!contentType.includes("text/html")) return upstream;

    let rw = new HTMLRewriter();

    if (cfg.title) {
      rw = rw
        .on("title", {
          element(el) { el.setInnerContent(cfg.title); }
        })
        .on('meta[property="og:title"]', {
          element(el) { el.setAttribute("content", cfg.title); }
        })
        .on('meta[name="twitter:title"]', {
          element(el) { el.setAttribute("content", cfg.title); }
        });
    }

    if (cfg.description) {
      rw = rw
        .on('meta[name="description"]', {
          element(el) { el.setAttribute("content", cfg.description); }
        })
        .on('meta[property="og:description"]', {
          element(el) { el.setAttribute("content", cfg.description); }
        })
        .on('meta[name="twitter:description"]', {
          element(el) { el.setAttribute("content", cfg.description); }
        });
    }

    if (cfg.linkHtml) {
      let inserted = false;
      rw = rw.on("h2", {
        element(el) {
          if (!inserted) {
            el.before(cfg.linkHtml, { html: true });
            inserted = true;
          }
        }
      });
    }

    const transformed = rw.transform(upstream);
    const headers = new Headers(transformed.headers);
    headers.delete("content-length");
    headers.delete("etag");
    headers.set("cache-control", "no-store");
    headers.set("x-robots-tag", "noindex, nofollow");
    headers.set("x-aivs-v33-status", "patched-v3");

    return new Response(transformed.body, {
      status: transformed.status,
      statusText: transformed.statusText,
      headers
    });
  }
};
