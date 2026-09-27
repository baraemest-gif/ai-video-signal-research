# AI Video Signal Filmora single-route overlay

Purpose: reinforce `/filmora-free-vs-paid/` from the already-ranking `/filmora-ai-credits/` page without uploading or replacing the existing Cloudflare Pages site.

Safety:
- preview config has no custom-domain route;
- production config targets only `aivideosignal.com/filmora-ai-credits*`;
- no title, H1, canonical, CSS, JS, Worker, or other Pages files are replaced;
- if the expected HTML marker is absent, the overlay returns the origin HTML unchanged;
- production deploy is intentionally NOT automated in this branch.
