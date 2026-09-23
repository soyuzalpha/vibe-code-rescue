# Case study — audit report as delivered

Read-only audit of a live Next.js 16 app (127 source files, 11,606 LOC, 18 Prisma
models, 11 API routes). Kept here as the source of truth for the published page
`public/case-study.html` and for re-use in real client work.

**Rules followed** (per `audit-checklist.md`): every finding carries evidence;
nothing on the app was changed, deployed or deleted; secrets are located and
redacted, never printed; severity comes from the table, not from feeling.

**Result: 6 findings — 0 Critical, 3 High, 2 Medium, 1 Low. ~6.25 h ≈ $400.**

---

## F-1 — Secrets are baked into the production image

Severity: **High**
Where: `.dockerignore` is 0 bytes → `Dockerfile:16` `COPY . .` → `.env`,
`.env.local` and `.git` all end up inside image `clipper:latest`.

```
$ stat -c %s .dockerignore
0
$ docker exec clipper ls -la /app/.env /app/.env.local
-rw-rw-r-- 1 root root 1392 Sep 14 10:04 /app/.env
-rw-rw-r-- 1 root root  962 Sep 16 11:18 /app/.env.local
$ docker exec clipper sh -c '[ -d /app/.git ] && find /app/.git -type f | wc -l'
28
```

Impact: `AUTH_SECRET` lives inside the image layers. Anyone who can read the
image — a registry, a host, a backup, `docker save` — can forge a session cookie
for any account, and gets the full git history with it.
Fix: a real `.dockerignore` (`.env*`, `.git`, `node_modules`, `.next`) + rebuild
+ **rotate `AUTH_SECRET`** (the old one must be treated as burned).
Estimate: 1 h.

## F-2 — Uploads are written to a path that is not mounted, so every deploy deletes them

Severity: **High**
Where: `src/lib/storage/service.ts:10` — root is `./storage` when
`CONTENT_STORAGE_PATH` is unset; the only mount on the container is `/app/data`.

```
$ docker exec clipper printenv CONTENT_STORAGE_PATH
(empty)
$ docker inspect clipper --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}'
/home/cosmic/app/clipper/data -> /app/data
$ docker exec clipper sh -c 'find /app/storage -type f | wc -l'
0
```

Impact: the database survives (`file:./data/content.db`, which *is* mounted), the
files do not. Every uploaded video, thumbnail and avatar is written into the
container's writable layer and destroyed on the next deploy — leaving database
rows pointing at files nobody can open. Latent only because nothing has been
uploaded yet.
Fix: `CONTENT_STORAGE_PATH=/app/data/storage` + mount it.
Estimate: 1 h.

## F-3 — The app thinks it is running on `http://localhost:3000`

Severity: **High**
Where: container env `NEXT_PUBLIC_BASE_URL`; consumed at
`src/lib/social/oauth.ts:27` and `src/app/api/auth/[platform]/callback/route.ts:20`.

```
$ docker exec clipper printenv NEXT_PUBLIC_BASE_URL
http://localhost:3000

$ curl -sI https://clipper.soyuz.my.id/api/content | grep -i location
location: /login?callbackUrl=https%3A%2F%2Flocalhost%3A3000%2Fapi%2Fcontent

$ curl -s -o /dev/null -D - -H 'Host: clipper.soyuz.my.id' \
    http://127.0.0.1:3000/api/content | grep -i location
location: /login?callbackUrl=http%3A%2F%2Flocalhost%3A3000%2Fapi%2Fcontent

$ curl -s -o /dev/null -D - -X POST \
    https://clipper.soyuz.my.id/api/auth/callback/credentials ... | grep -i location
location: https://localhost:3000/login?error=CredentialsSignin&code=credentials
```

The origin is `localhost:3000` even when the request carries
`Host: clipper.soyuz.my.id`, so the app is not reading the host header — the
value comes from `NEXT_PUBLIC_BASE_URL`, and the code's dev fallback is the same
string, which is why it went unnoticed.

Impact: two user-visible breaks. A mistyped password sends the browser to
`https://localhost:3000` — an unreachable host — instead of showing "Invalid
email or password". And the `redirect_uri` handed to TikTok/Instagram/YouTube is
`http://localhost:3000/api/auth/<platform>/callback`, which no provider accepts,
so connecting a social account can never complete in production.
Fix: `NEXT_PUBLIC_BASE_URL=https://clipper.soyuz.my.id` + rebuild.
Estimate: 1 h.

## F-4 — The env schema guards 2 of the 12 variables the code reads

Severity: **Medium**
Where: `src/lib/env.ts:3-15` validates only `DATABASE_URL` and `AUTH_SECRET`.

```
code reads:   AI_PROVIDER AI_GATEWAY_MODEL AI_GATEWAY_BASE_URL AI_GATEWAY_API_KEY
              DATABASE_URL NODE_ENV NEXT_PUBLIC_BASE_URL CONTENT_STORAGE_PATH
              CONTENT_MAX_UPLOAD_MB (+6 OAuth vars)
in container: AUTH_SECRET AUTH_TRUST_HOST DATABASE_URL NEXT_PUBLIC_BASE_URL
              NODE_ENV (+ base image vars)
```

Impact: this is *why* F-2 and F-3 shipped. A missing or dev-default integration
variable raises nothing at boot — the app starts, looks healthy, and fails only
when a user walks into that path.
Fix: extend the zod schema to every variable the code reads; fail fast at boot.
Estimate: 2 h.

## F-5 — Production runs the AI features on mock data

Severity: **Medium**
Where: `src/lib/ai/config.ts:38` (`process.env.AI_PROVIDER ?? "mock"`),
`src/lib/ai/providers/mock.ts`.

```
$ docker exec clipper printenv AI_PROVIDER
(empty)  → getAIConfig() returns provider "mock"
```

`mock.ts` is explicit about it: *"Returns deterministic, schema-valid mock data
with just enough variance to feel alive."* Ideas, hooks, scripts, viral scores and
analytics patterns are generated locally and returned through the same response
shape as a real model.

Impact: anyone using the idea / script / analysis features gets fabricated output
presented as analysis. Fine for a demo, but nothing in the UI says so.
Fix: set `AI_PROVIDER=hemattoken` + the gateway vars, or label mock mode in the UI.
Estimate: 1 h.

## F-6 — A developer machine's address left in the production config

Severity: **Low**
Where: `next.config.ts` — `allowedDevOrigins: ["100.87.252.65"]`.

Impact: none today. It is a hard-coded personal IP shipped in the config, and it
widens what the dev-origin check accepts.
Fix: drop it, or gate it behind `NODE_ENV !== "production"`.
Estimate: 0.25 h.

---

## What passed (no action needed)

Said plainly, because a report that only lists problems is not a measurement.

- **No secret reaches the browser.** All 9 shipped JS chunks were downloaded from
  the live site and scanned for key patterns. The 9 raw hits were all
  `mask-image-linear-from-pos` matching a `sk-` pattern — zero real matches.
  Source maps are not published (`404`).
- **Every route is gated on the server.** `src/proxy.ts` runs the Auth.js
  middleware over everything except `/api/auth/*`; all 10 API paths probed
  without a session returned `307 → /login`. Server actions call `requireAuth()`
  as well, so there is no client-only guard anywhere.
- **Path traversal is refused.** `storage.resolve()` rejects any key that escapes
  the storage root.
- **The integrations do not fail silently.** No empty `catch {}` blocks; all 7
  external `fetch` calls check `response.ok` and throw with the status code.
- **Credentials stay out of git.** `.env` and `.env.local` are untracked and
  `.gitignore` covers `.env*`. F-1 is about the image, not the repository.
- **The alarming cache header is harmless.** `/login` ships
  `cache-control: s-maxage=31536000`, but Cloudflare reports
  `cf-cache-status: DYNAMIC` on repeated requests — the page is never cached, so
  no stale CSRF token can be served.

## Totals

| Finding | Severity | Estimate |
|---|---|---|
| F-1 image ships `.env`, `.env.local`, `.git` | High | 1 h — $75 |
| F-2 uploads on an unmounted path | High | 1 h — $75 |
| F-3 origin resolves to `localhost:3000` | High | 1 h — $75 |
| F-4 env schema guards 2 of 12 vars | Medium | 2 h — $150 |
| F-5 AI runs on mock data in production | Medium | 1 h — $75 |
| F-6 personal IP in shipped config | Low | 0.25 h — $20 |
| | | **~6.25 h — ~$400** |

## Recommendation

Fix F-1, F-2 and F-3 first — three hours, and they are one `.dockerignore`, two
environment variables and a rebuild. Nothing here needs a rewrite, and none of it
is a code-quality problem: the code is careful, the *deployment* drifted away
from it. Then F-4, so the same class of drift fails loudly instead of silently.
F-5 needs a product decision before it needs code. F-6 is cleanup.

## What was not checked

No access to database contents beyond row counts. No penetration testing of the
AI gateway. No review of Prisma indexing or of the business logic inside the 11
API routes. No load testing. No mobile or accessibility pass on the dashboard UI.
The OAuth flows could not be exercised end to end — no provider credentials are
configured, which is itself part of F-3 and F-4.
