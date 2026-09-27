const UPSTREAM = "https://57ec6ea9.ai-video-signal.pages.dev";

function replaceRequired(body, variants, replacements) {
  let out = body;
  let found = false;
  for (let i = 0; i < variants.length; i++) {
    const from = variants[i];
    if (out.includes(from)) {
      found = true;
      out = out.split(from).join(replacements[i] ?? replacements[0]);
    }
  }
  return { body: out, found };
}

function escapeRegex(s) {
  return s.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
}

function insertBeforeHeading(body, heading, paragraph) {
  if (body.includes("v33-sales-ctr")) return { body, found: true };
  const re = new RegExp("(<h2\\b[^>]*>\\s*" + escapeRegex(heading) + "\\s*</h2>)", "i");
  if (!re.test(body)) return { body, found: false };
  return { body: body.replace(re, paragraph + "$1"), found: true };
}

function patchRoute(path, body) {
  const original = body;
  let out = body;
  let result;

  if (path === "/elevenlabs-cancellation-refund-policy/") {
    result = replaceRequired(
      out,
      [
        "ElevenLabs Cancellation &amp; Refund Policy 2026: 14-Day Rule",
        "ElevenLabs Cancellation & Refund Policy 2026: 14-Day Rule"
      ],
      [
        "ElevenLabs Refund Policy 2026: 14-Day Rule, Cancellation &amp; Credits",
        "ElevenLabs Refund Policy 2026: 14-Day Rule, Cancellation & Credits"
      ]
    );
    if (!result.found) return { body: original, ok: false, reason: "title" };
    out = result.body;

    result = replaceRequired(
      out,
      ["ElevenLabs cancellation and refund policy for 2026: how to cancel, the 14-day unused-credit refund rule, credit loss, mobile purchases and EU rights."],
      ["ElevenLabs refund policy 2026: see the 14-day unused-credit rule, how cancellation works, what happens to credits, and mobile/EU refund paths."]
    );
    if (!result.found) return { body: original, ok: false, reason: "description" };
    out = result.body;
    return { body: out, ok: true };
  }

  if (path === "/filmora-free-vs-paid/") {
    result = replaceRequired(
      out,
      [
        "Filmora Free vs Paid 2026: Watermark, Limits &amp; Price",
        "Filmora Free vs Paid 2026: Watermark, Limits & Price"
      ],
      [
        "Filmora Free vs Paid 2026: Watermark, Price &amp; Is It Worth It?",
        "Filmora Free vs Paid 2026: Watermark, Price & Is It Worth It?"
      ]
    );
    if (!result.found) return { body: original, ok: false, reason: "title" };
    out = result.body;

    result = replaceRequired(
      out,
      ["Filmora Free vs Paid in 2026: compare free-version limitations, watermark rules, exports, AI credits and paid-plan differences before you upgrade."],
      ["Filmora Free vs Paid 2026: compare watermark rules, export limits, AI credits, current pricing and when upgrading is actually worth it."]
    );
    if (!result.found) return { body: original, ok: false, reason: "description" };
    out = result.body;
    return { body: out, ok: true };
  }

  if (path === "/best-ai-video-tools-for-compliance-training/") {
    result = replaceRequired(
      out,
      ["A practical comparison of AI video platforms for compliance training, policy updates and multilingual employee education."],
      ["Compare AI compliance video tools for policy/SOP training, SCORM/LMS delivery, completion tracking, localization, version updates and knowledge checks."]
    );
    return result.found ? { body: result.body, ok: true } : { body: original, ok: false, reason: "description" };
  }

  if (path === "/filmora-free-trial/") {
    result = replaceRequired(
      out,
      ["Filmora free trial, watermark rules, account rewards and buying guidance for 2026."],
      ["Filmora free trial guide for 2026: watermark rules, the current free-export reward, achievement trials, Creative Assets trial and when to upgrade."]
    );
    return result.found ? { body: result.body, ok: true } : { body: original, ok: false, reason: "description" };
  }

  if (path === "/ai-video-pricing-benchmarks/") {
    result = insertBeforeHeading(
      out,
      "What the benchmark actually says",
      '<p class="internal-authority-link v33-sales-ctr">Before choosing from the benchmark, <a href="/best-ai-video-generators/">compare AI video generators by workflow and pricing</a> to match subscription cost with the job you actually need to do.</p>'
    );
    return result.found ? { body: result.body, ok: true } : { body: original, ok: false, reason: "heading" };
  }

  if (path === "/ai-video-annual-vs-monthly-pricing-comparison/") {
    result = insertBeforeHeading(
      out,
      "Evidence behind this decision",
      '<p class="internal-authority-link v33-sales-ctr">If you have not settled on a provider yet, <a href="/best-ai-video-generators/">compare the leading AI video generators before choosing a billing term</a>; annual savings matter only after the workflow fit is proven.</p>'
    );
    return result.found ? { body: result.body, ok: true } : { body: original, ok: false, reason: "heading" };
  }

  if (path === "/ai-video-credits-usage-comparison/") {
    result = insertBeforeHeading(
      out,
      "How six AI usage systems compare",
      '<p class="internal-authority-link v33-sales-ctr">For the broader purchase decision, <a href="/best-ai-video-generators/">compare AI video generators by pricing model and workflow</a> before treating any vendor credit as equivalent value.</p>'
    );
    return result.found ? { body: result.body, ok: true } : { body: original, ok: false, reason: "heading" };
  }

  return { body: out, ok: true };
}

function isTarget(path) {
  return [
    "/elevenlabs-cancellation-refund-policy/",
    "/filmora-free-vs-paid/",
    "/best-ai-video-tools-for-compliance-training/",
    "/filmora-free-trial/",
    "/ai-video-pricing-benchmarks/",
    "/ai-video-annual-vs-monthly-pricing-comparison/",
    "/ai-video-credits-usage-comparison/"
  ].includes(path);
}

async function proxy(request) {
  const u = new URL(request.url);
  const upstream = UPSTREAM + u.pathname + u.search;
  const headers = new Headers(request.headers);
  headers.set("host", new URL(UPSTREAM).host);
  const init = { method: request.method, headers, redirect: "manual" };
  if (!["GET", "HEAD"].includes(request.method)) init.body = request.body;
  return fetch(upstream, init);
}

export default {
  async fetch(request) {
    const u = new URL(request.url);
    const upstream = await proxy(request);

    if (request.method !== "GET" || !isTarget(u.pathname)) return upstream;

    const ct = upstream.headers.get("content-type") || "";
    if (!ct.includes("text/html")) return upstream;

    const original = await upstream.text();
    const patched = patchRoute(u.pathname, original);
    const headers = new Headers(upstream.headers);
    headers.delete("content-length");
    headers.delete("content-encoding");
    headers.delete("etag");
    headers.set("cache-control", "no-store");

    if (!patched.ok) {
      headers.set("x-aivs-v33-status", "guard-failed");
      headers.set("x-aivs-v33-reason", patched.reason || "unknown");
      return new Response(original, { status: upstream.status, headers });
    }

    headers.set("x-aivs-v33-status", "patched-v2");
    return new Response(patched.body, { status: upstream.status, headers });
  }
};
