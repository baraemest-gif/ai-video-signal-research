const UPSTREAM = "https://57ec6ea9.ai-video-signal.pages.dev";

const patches = {
  "/elevenlabs-cancellation-refund-policy/": [
    ["<title>ElevenLabs Cancellation &amp; Refund Policy 2026: 14-Day Rule</title>", "<title>ElevenLabs Refund Policy 2026: 14-Day Rule, Cancellation &amp; Credits</title>"],
    ['content="ElevenLabs cancellation and refund policy for 2026: how to cancel, the 14-day unused-credit refund rule, credit loss, mobile purchases and EU rights."', 'content="ElevenLabs refund policy 2026: see the 14-day unused-credit rule, how cancellation works, what happens to credits, and mobile/EU refund paths."']
  ],
  "/filmora-free-vs-paid/": [
    ["<title>Filmora Free vs Paid 2026: Watermark, Limits &amp; Price</title>", "<title>Filmora Free vs Paid 2026: Watermark, Price &amp; Is It Worth It?</title>"],
    ['content="Filmora Free vs Paid in 2026: compare free-version limitations, watermark rules, exports, AI credits and paid-plan differences before you upgrade."', 'content="Filmora Free vs Paid 2026: compare watermark rules, export limits, AI credits, current pricing and when upgrading is actually worth it."']
  ],
  "/best-ai-video-tools-for-compliance-training/": [
    ['content="A practical comparison of AI video platforms for compliance training, policy updates and multilingual employee education."', 'content="Compare AI compliance video tools for policy/SOP training, SCORM/LMS delivery, completion tracking, localization, version updates and knowledge checks."']
  ],
  "/filmora-free-trial/": [
    ['content="Filmora free trial, watermark rules, account rewards and buying guidance for 2026."', 'content="Filmora free trial guide for 2026: watermark rules, the current free-export reward, achievement trials, Creative Assets trial and when to upgrade."']
  ],
  "/ai-video-pricing-benchmarks/": [
    ['<h2>What the benchmark actually says</h2>', '<p class="internal-authority-link v33-sales-ctr">Before choosing from the benchmark, <a href="/best-ai-video-generators/">compare AI video generators by workflow and pricing</a> to match subscription cost with the job you actually need to do.</p><h2>What the benchmark actually says</h2>']
  ],
  "/ai-video-annual-vs-monthly-pricing-comparison/": [
    ['<h2>Evidence behind this decision</h2>', '<p class="internal-authority-link v33-sales-ctr">If you have not settled on a provider yet, <a href="/best-ai-video-generators/">compare the leading AI video generators before choosing a billing term</a>; annual savings matter only after the workflow fit is proven.</p><h2>Evidence behind this decision</h2>']
  ],
  "/ai-video-credits-usage-comparison/": [
    ['<h2>How six AI usage systems compare</h2>', '<p class="internal-authority-link v33-sales-ctr">For the broader purchase decision, <a href="/best-ai-video-generators/">compare AI video generators by pricing model and workflow</a> before treating any vendor credit as equivalent value.</p><h2>How six AI usage systems compare</h2>']
  ]
};

function upstreamUrl(request) {
  const u = new URL(request.url);
  return UPSTREAM + u.pathname + u.search;
}

async function proxy(request) {
  const url = upstreamUrl(request);
  const init = {
    method: request.method,
    headers: new Headers(request.headers),
    redirect: "manual"
  };
  init.headers.set("host", new URL(UPSTREAM).host);
  if (!["GET","HEAD"].includes(request.method)) init.body = request.body;
  return fetch(url, init);
}

export default {
  async fetch(request) {
    const u = new URL(request.url);
    const upstream = await proxy(request);

    if (request.method !== "GET" || !patches[u.pathname]) {
      return upstream;
    }

    const ct = upstream.headers.get("content-type") || "";
    if (!ct.includes("text/html")) return upstream;

    let body = await upstream.text();
    const rules = patches[u.pathname];
    const missing = rules.filter(([from]) => !body.includes(from));

    if (missing.length) {
      const h = new Headers(upstream.headers);
      h.set("x-aivs-v33-status", "guard-failed");
      h.set("x-aivs-v33-missing", String(missing.length));
      return new Response(body, {status: upstream.status, headers: h});
    }

    for (const [from,to] of rules) body = body.replace(from,to);

    // Keep social metadata aligned with the new standard meta when exact originals exist.
    if (u.pathname === "/elevenlabs-cancellation-refund-policy/") {
      body = body.replaceAll(
        "ElevenLabs Cancellation &amp; Refund Policy 2026: 14-Day Rule",
        "ElevenLabs Refund Policy 2026: 14-Day Rule, Cancellation &amp; Credits"
      ).replaceAll(
        "ElevenLabs cancellation and refund policy for 2026: how to cancel, the 14-day unused-credit refund rule, credit loss, mobile purchases and EU rights.",
        "ElevenLabs refund policy 2026: see the 14-day unused-credit rule, how cancellation works, what happens to credits, and mobile/EU refund paths."
      );
    }
    if (u.pathname === "/filmora-free-vs-paid/") {
      body = body.replaceAll(
        "Filmora Free vs Paid 2026: Watermark, Limits &amp; Price",
        "Filmora Free vs Paid 2026: Watermark, Price &amp; Is It Worth It?"
      ).replaceAll(
        "Filmora Free vs Paid in 2026: compare free-version limitations, watermark rules, exports, AI credits and paid-plan differences before you upgrade.",
        "Filmora Free vs Paid 2026: compare watermark rules, export limits, AI credits, current pricing and when upgrading is actually worth it."
      );
    }

    const h = new Headers(upstream.headers);
    h.delete("content-length");
    h.set("x-aivs-v33-status", "patched");
    h.set("cache-control", "no-store");
    return new Response(body, {status: upstream.status, headers: h});
  }
};
