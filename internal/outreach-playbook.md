# Outreach playbook — Vibe Code Rescue

Companion to `outreach-templates.md` (the 20 drafts). This file is the part that
matters more: **where each draft is actually allowed**, and what has to change
before it gets posted. Rules were read from each community's own public pages, not
guessed. Sources are listed so they can be re-checked.

**Hard truth up front.** Every channel here is gated on something only you have:
a Reddit account with real history, an X account, a Discord account, an Upwork
profile. A brand-new account posting a pitch gets auto-removed and can get the
domain blacklisted. The order below is therefore built around the one play that
works from a cold account: **answer the question, don't pitch.**

---

## The one template that works everywhere

Templates 1–15 in `outreach-templates.md` end with a price and an offer. In
r/vibecoding and r/webdev that gets removed. Use this instead — it is the same
knowledge with the pitch stripped, and it is allowed nearly everywhere:

```
First thing to check on a Lovable/Bolt export: the browser bundle. Open the built
JS and look for anything key-shaped — anything prefixed NEXT_PUBLIC_ or VITE_ ships
to the client. If a Stripe or Supabase service key is in there, rotate it today,
then move the call behind a server route.

After that: is RLS actually on, per table? Test it with the anon key and confirm you
get zero rows you don't own.

Then diff the prod env names against local — that's where "works on my machine"
usually lives.

All three are checkable in an afternoon. Happy to point at the specific file if you
paste your repo structure.
```

No link. No price. No product name. If someone replies *"do you do this for hire?"*
— that is the invitation, and only then do you answer with the $150 audit. That
sequence is what the mods of both subs actually ask for.

---

## Channel rules (read from source)

| Channel | What the rules say | Play |
|---|---|---|
| **r/vibecoding** | Self-promo restricted. Tool promotion needs mod pre-approval via the X "Vibe Coding Community". Project posts must include educational content — link drops are removed. | Answer questions with no link. Never post the service. |
| **r/webdev** | Self-promo only inside **Showoff Saturday**. Outside it, non-promotional contributions only. | Answer hard technical questions. Save any project post for Saturday. |
| **r/SaaS** | Self-promo limited to **once per 60 days** — and that count includes comment plugs, links *and mentions* of your product. | One mention maximum, ever, in a thread where it is genuinely the answer. |
| **r/Supabase** | Active RLS/policy threads. No blanket ban found, but the same 90/10 expectation applies. | Answer RLS questions completely. |
| **Lovable Discord** | `discord.gg/lovable-dev`. The community describes itself as *not* a support platform — help comes from fellow builders. | Answer in #help first. Only mention the paid audit if someone is clearly stuck. Never DM uninvited. |
| **X** | No gate on replies. | Reply to specific posts, 3 lines, no link in the first reply. |
| **Upwork / Fiverr** | Job boards — a proposal *is* the product. | Templates 19–20 apply as written. |

Sources: r/vibecoding rule update (gist.github.com/popmechanic/21277a7f…), the
mod's own post (reddit.com/r/vibecoding/comments/1mp8oyw), r/SaaS
(reddit.com/r/SaaS/comments/1slno92), r/webdev Showoff Saturday guidance,
lovable.dev/discord.

**The 90/10 rule** applies to every subreddit here: fewer than 1 in 10 of your
posts may touch your own product. Brand-new accounts that only post about the
service get removed on sight.

---

## Target list

Each entry is a real thread or community surfaced while researching. **Re-verify
before posting** — these came from a web index, not from a logged-in session, so
the thread may be older, locked or deleted. Open it logged out first; a removed
comment still looks normal on your own profile.

> Verified this pass: the two Discord invites return `200` (`discord.gg/lovable-dev`
> and `lovable.dev/discord`). **Reddit blocks every automated fetch** — plain `curl`
> gets a `000`, and the extraction backend gets a `403` — so the Reddit URLs below
> were confirmed to exist in the search index but must be opened by hand before
> replying. The thread IDs are correct; the live state is not machine-checkable.

### Highest intent — people describing exactly the service

| # | Target | Why it fits | Draft |
|---|---|---|---|
| 1 | r/vibecoding — "Can vibe-coded apps actually survive production?" (`/comments/1tumgz0`) | The whole thread is the question this service answers: security, deployment, maintenance. | No-link answer (above) + name the four failure points. |
| 2 | r/vibecoding — "Vibe coding kept handing me apps that looked finished but didn't work" (`/comments/1ulj42l`) | Auth that's a form, buttons that do nothing, data that vanishes — the "looks done, isn't" class. | No-link answer. This is the "what actually breaks" list. |
| 3 | r/vibecoding — "My Lovable app broke at 3am and I had no idea how to fix it" (`/comments/1so5h1r`) | Deployed, has users, things started breaking. Post is itself a pitch for a competitor tool — reply to the *problem*, not the tool. | No-link answer. |
| 4 | r/vibecoding — "Your app works, but your code is messy" (`/comments/1s2s15u`) | A senior dev posting a pre-scale checklist. Contribute a fifth check (leaked keys, RLS) — no pitch. | No-link answer, add the security check they omitted. |
| 5 | r/Supabase — "Need clarifications on Row Level Security" (`/comments/1ppq2qv`) | RLS confusion is the #1 finding class. | No-link answer; the one place a link is safe is **if they ask for one**. |
| 6 | r/Supabase — "Supabase RLS is not for production" (`/comments/1mvjpr8`) | Contested thread, lots of wrong answers. Being the correct one earns profile clicks. | No-link answer. |
| 7 | r/Supabase — "service_role API key not bypassing RLS" (`/comments/1crhv56`) | A service-role key in the wrong place is the exact leak this service finds. | No-link answer. |

### X — reply, don't post

| # | Target | Why it fits |
|---|---|---|
| 8 | Posts about `NEXT_PUBLIC_` leaking secrets — the thread runs through @manoj_ahi (1903333877558501697), @leojr94_ (1917142580971610163), and @rauchg's v0 security post (1909313757496610917) | Template 1. The reply is the useful correction; the audit is a second reply only if asked. |
| 9 | @vercel_dev (1752130550641447082) — Vercel warning that prefixed env vars reach the client | Template 1, softer. |
| 10 | Anyone posting a Supabase "is my data exposed?" panic | Template 2. |
| 11 | Anyone posting "works locally, breaks in production" | Template 3. |
| 12 | Anyone posting lost signups / a form that does nothing | Template 4. |
| 13 | Anyone posting "Stripe says paid but my app doesn't know" | Template 5. |
| 14 | Builders who shipped with an AI tool and hit the wall | Template 6. |

For 10–14 there is no fixed URL — search live in the X app for the phrase, then
reply. `xurl search "NEXT_PUBLIC_ leak" -n 20` works once auth is set up.

### Discord

| # | Target | Why it fits |
|---|---|---|
| 15 | Lovable Discord `discord.gg/lovable-dev` → #help | Template 12. Biggest concentration of the exact target user. Answer, then wait to be asked. |
| 16 | Bolt and v0 community servers → #help | Templates 13–14. |
| 17 | Supabase community server → #help | Template 15. |

### Cold DM (Indonesian) — people you actually know

| # | Target | Why it fits |
|---|---|---|
| 18 | Anyone whose app you have seen go live | Template 16. |
| 19 | Anyone who has complained about a production bug | Template 17. |
| 20 | Anyone selling a SaaS with no technical owner | Template 18. |

Only people you genuinely know. One message, no follow-up.

### Paid channels

| # | Target | Notes |
|---|---|---|
| 21 | Fiverr gig | Template 19. Needs the gig listing built first. |
| 22 | Upwork profile + proposals | Template 20. Needs a profile; proposals are where the money actually starts. |

---

## Order to work it

1. **r/vibecoding and r/Supabase answers** — targets 1–7. Zero risk, and it builds
   the account history that makes everything else survivable. Two answers a day for
   a week beats any amount of pitching.
2. **X replies** — targets 8–14. No account history needed, and the threads are
   time-sensitive.
3. **Discord** — targets 15–17. Answer-only until someone asks.
4. **Cold DMs** — 18–20. Lowest volume, highest conversion, zero cost.
5. **Upwork** — 22. Needs a profile built; the highest ceiling of anything here.
6. **Fiverr** — 21. Last, because a gig with no reviews converts poorly.

## What has to happen by hand

These need your own accounts and cannot be automated from here:

- **X**: register the app at developer.x.com, then run `xurl auth apps add`,
  `xurl auth oauth2 --app <name>` and `xurl auth default <name>`. The CLI is
  installed at `~/.local/bin/xurl` (v1.3.1) but has no credentials — and secrets
  must not pass through this chat, so that step is yours.
- **Reddit**: build 1–2 weeks of genuine answer history before any post that
  mentions the service.
- **Discord**: join and read #help for a day before answering.

## Rules that override everything

- Never post the same text twice in one thread.
- Never invent a client, a testimonial, or a result.
- One reply per thread. No bumping.
- If the template doesn't match what the person actually wrote, don't send it.
- If a community's rule contradicts a template, the rule wins.
