# Outreach Templates — Vibe Code Rescue

20 ready-to-send templates. Rules for all of them:

- **3 lines.** Not a pitch. Not a paragraph.
- Open by naming the **specific** thing they wrote. Never a generic greeting.
- Mention **$150** and the **money-back guarantee**.
- English for X / Reddit / Discord / Fiverr-Upwork. Indonesian for cold DMs to people you know.
- No spam, no pretending to be someone else, no promises you can't keep.
- Never post the same text twice in one thread. If it doesn't fit the post, skip it.

---

## X / Twitter (6)

### 1. Leaked API key in the bundle
**Platform:** X — reply to someone who posted a key or found one in their own app
**When:** they posted a screenshot, a repo, or said "wait, my key is in the JS?"

```
Yeah that's a frontend bundle leaking it — anything prefixed NEXT_PUBLIC_/VITE_ ships to the browser.
Rotate the key today, then move the call behind a server route.
I do a $150 48h audit that catches exactly this + auth + dead integrations. Money back if nothing serious. Happy to look at yours.
```

### 2. Supabase RLS off / everyone can read everything
**Platform:** X — reply to Supabase users asking about RLS or posting a "my table is public" panic
**When:** they mention RLS, policies, or seeing other users' rows

```
If RLS is off, your anon key reads every row in the table — the key being public isn't the problem, the missing policy is.
Write the policy per table first, then check with the anon key and confirm you get 0 rows you shouldn't.
$150 audit covers RLS + auth + leaked secrets in 48h, money back if there's nothing serious.
```

### 3. "Works locally, breaks in production"
**Platform:** X — reply to "runs fine on localhost but prod is broken"
**When:** env / build / deploy mismatch symptoms

```
Classic env split: prod is missing the vars local has, or it's serving a stale build.
Diff the env names prod vs local first, then check the deploy is actually running the new commit.
I do a $150 48h audit that ends with a list of what's broken and what each fix costs. Money back if I find nothing serious.
```

### 4. Form silently failing
**Platform:** X — reply to someone who lost signups/leads
**When:** "nobody's signing up", "the form does nothing"

```
If the form "submits" with no error and no record, the handler is probably 404-ing or the table write is being rejected silently.
Open devtools → Network on submit and look at the actual status code before touching the code.
$150 48h audit finds this + the other silent failures. Money back if nothing serious turns up.
```

### 5. Stripe / webhook failing silently
**Platform:** X — reply to missing-payment or webhook complaints
**When:** they mention payments not landing, webhooks, or "Stripe says paid but my app doesn't know"

```
Webhooks fail quietly by default — wrong signature secret, or the endpoint isn't reachable, and the order just never updates.
Check the webhook delivery log in the dashboard; the failed attempts will tell you which one it is.
$150 48h audit maps your payment path end to end. Money back if there's nothing serious.
```

### 6. "AI built it, now I'm stuck"
**Platform:** X — reply to a builder who shipped with an AI tool and hit the wall
**When:** they're stuck, overwhelmed, don't know where to start

```
You don't need a rewrite — you need to know which five things are actually broken before you touch anything else.
I read AI-generated code all day; the same handful of holes show up every time.
$150, 48 hours, written report, money back if there's nothing serious in it.
```

---

## Reddit (5)

> Reddit rule: read the sub's self-promo policy first. If promotion isn't allowed, answer the question fully with no pitch — that comment still wins work later.

### 7. r/vibecoding — someone posting a broken AI-built app
**Platform:** r/vibecoding
**When:** a "help, my vibe-coded app is falling apart" post

```
The first thing I'd check on a vibe-coded app is the browser bundle: search the built JS for any key that shouldn't be public — that's the most common and most expensive one.
After that it's RLS/auth, then env vars in prod, then the integrations that fail without throwing.
I do a $150 48-hour audit that produces exactly that list with fix costs. Money back if there's nothing serious. Happy to point you at the right file if you paste your repo structure.
```

### 8. r/SaaS — founder losing signups or payments
**Platform:** r/SaaS
**When:** a post about conversion, churn, or "people sign up but nothing happens"

```
Before you blame the copy: check whether the signup actually completes. A form that 404s its handler loses leads with zero error anywhere.
Open the network tab, submit, and look at the status code — that alone answers half of these threads.
If you want the full picture, I run a $150 48-hour audit (money back if nothing serious) covering forms, auth, leaks and dead integrations.
```

### 9. r/IndieHackers — solo dev stuck before launch
**Platform:** r/IndieHackers
**When:** pre-launch jitters, "is my app ready?" posts

```
"Ready" usually means four things: no secrets in the frontend, auth actually enforced, prod env matching local, and every external call erroring loudly instead of silently.
You can self-check all four in an afternoon — most people find at least one broken.
I do the same pass as a $150 48-hour written audit if you'd rather not; money back if I find nothing serious.
```

### 10. r/webdev — technical thread about AI-generated code quality
**Platform:** r/webdev
**When:** discussion about LLM code, security of generated apps

```
The pattern in AI-generated apps is consistent: the happy path is solid, the failure paths and the security boundary are not. Missing RLS policies, client-side secrets, unhandled webhook errors.
You can grep for it — search the production bundle for anything that looks like a key, and check every table's RLS state.
I turn that into a paid $150 48-hour audit with severity and fix estimates; money back if nothing serious shows up.
```

### 11. r/Supabase — RLS / auth questions
**Platform:** r/Supabase
**When:** RLS policy confusion, "is my data exposed?"

```
Quick test: use the anon key from the browser and try to select rows you shouldn't own. If you get them, RLS is off or the policy is permissive — the key being public is fine, that's what it's for.
Do that per table before anything else; a single missing policy is usually the whole exposure.
I do a $150 48-hour audit covering RLS, auth and leaked keys. Money back if there's nothing serious in it.
```

---

## Discord (4)

> Discord rule: answer in #help, help first. Only mention the paid audit if the person is clearly stuck after a real attempt. Never DM without being asked.

### 12. Lovable server — #help
**Platform:** Discord — Lovable official / community server, #help
**When:** someone can't get their exported Lovable app working outside the preview

```
Exporting out of Lovable almost always breaks on env vars — the preview injects them, your host doesn't. Copy the exact names into your host's dashboard and redeploy.
If the app still misbehaves after that, the next suspects are client-side secrets and unenforced RLS.
I do a $150 48-hour audit that lists all of it with fix costs — money back if nothing serious. Ping me if you want it.
```

### 13. Bolt server — #help
**Platform:** Discord — Bolt community server, #help
**When:** Bolt-generated app deploys but behaves differently live

```
Bolt's dev server hides a lot: it's a different build, different env, sometimes a different runtime than production.
Rebuild locally with your production env vars before debugging anything else — half the "it broke on deploy" threads end there.
If you want the rest checked properly, I run a $150 48-hour audit; money back if nothing serious turns up.
```

### 14. v0 server — #help
**Platform:** Discord — v0 / Vercel community, #help
**When:** v0-generated UI works but backend calls fail in production

```
v0 gives you the UI; the API routes and env wiring are where it goes quiet in prod. Check the server logs, not the console — the error is almost always there.
Also confirm no secret got prefixed NEXT_PUBLIC_ and shipped to the client.
$150 48-hour audit covers both, money back if there's nothing serious.
```

### 15. Supabase server — #help
**Platform:** Discord — Supabase community server, #help
**When:** RLS, auth or policy questions

```
RLS is opt-in per table — a new table is open by default until you enable it and add a policy. That catches almost everyone coming from the dashboard.
Test with the anon key and confirm you get zero rows you don't own before you trust it.
I do a $150 48-hour audit covering RLS, auth and leaked keys — money back if nothing serious. Say the word.
```

---

## Cold DM — kenalan (3, Bahasa Indonesia)

> Aturan: cuma kirim ke orang yang lo tahu beneran punya app/SaaS. Satu pesan, jangan follow-up berkali-kali. Jangan pura-pura nanya padahal cuma mau jualan.

### 16. Kenalan yang app-nya baru rilis
**Platform:** WhatsApp / DM — kenalan yang baru launch produk
**Kapan:** dia baru cerita app-nya live

```
Bro, app lo udah live kan? Gue lagi buka jasa audit 48 jam buat app yang dibikin pakai AI builder.
Yang dicek: API key bocor di frontend, auth & RLS Supabase, env var produksi, form, dan integrasi yang mati diam-diam. Hasilnya laporan tertulis + estimasi biaya fix.
$150, kalau nggak nemu temuan serius duit lo balik. Mau gue cek punya lo?
```

### 17. Kenalan yang ngeluh app-nya error di production
**Platform:** WhatsApp / DM — kenalan yang lagi kesel sama bug produksi
**Kapan:** dia posting/cerita soal error di prod

```
Eh gue lihat lo kesel sama bug di prod — gue lagi buka jasa audit buat kasus kayak gitu, 48 jam.
Gue cek dari yang paling sering: secret di bundle, RLS mati, env var prod beda sama local, terus integrasi yang gagal tanpa error.
$150 flat, kalau nggak ada temuan serius duit balik. Gue bisa mulai minggu ini.
```

### 18. Kenalan yang punya SaaS tapi nggak ada yang ngurus teknis
**Platform:** WhatsApp / DM — kenalan yang SaaS-nya jalan sendiri tanpa tim teknis
**Kapan:** dia jualan tapi nggak punya developer

```
App lo jalan sendiri tanpa yang ngecekin teknis ya? Itu risiko yang paling sering kelewat.
Gue nawarin audit 48 jam: $150, dapet laporan apa yang rusak, apa risikonya, berapa biaya benerinnya. Kalau nggak ada temuan serius, duit balik.
Kalau lo mau, lanjutnya ada paket fix mingguan atau retainer bulanan — tapi audit dulu aja.
```

---

## Fiverr / Upwork (2)

### 19. Fiverr — gig description
**Platform:** Fiverr gig
**When:** setting up the gig listing

```
I will audit and fix your AI-built app before production breaks it

Built with Lovable, Bolt, v0 or Cursor? It demos great and fails with real users. I read AI-generated codebases and fix what they leave exposed: API keys leaking in the frontend bundle, broken auth and disabled Supabase Row Level Security, production env and DNS mess, forms that silently drop submissions, and integrations (Stripe, webhooks, APIs) that fail without an error.

Audit: $150, delivered in 48 hours — written report of what's broken, the risk of each item, and what it costs to fix. Full credit toward a fix if you continue. Money back if I find nothing serious.

Rescue Fix: $600–$1,200 flat, about one week, critical issues resolved with a fixed scope and fixed price. Keep-Alive retainer available at $300/month for monitoring and monthly repairs.

Send me your repo link and live URL and I'll tell you honestly what it needs.
```

### 20. Upwork — proposal reply
**Platform:** Upwork
**When:** applying to a job about fixing an AI-generated app

```
Hi — I fix exactly this: apps that were generated with AI tools and then break in production.

For a job like yours the first pass is always the same — search the production bundle for leaked keys, check auth and Supabase RLS, diff prod env against local, then trace every form and integration that fails quietly. That usually finds the real problem within a day.

I offer a $150 fixed-price audit delivered in 48 hours (money back if I find nothing serious), credited in full if you go ahead with the fix. Happy to start with that so you see the full picture before committing to anything bigger.
```

---

## Before you send anything

- Read the post twice. If the template doesn't match what they actually wrote, don't use it.
- One reply per thread. No bumping.
- Never claim a result you can't back up, never invent a client, never pretend to be a happy customer.
- If someone asks a question you can answer for free, answer it. The pitch can wait for the next message.
