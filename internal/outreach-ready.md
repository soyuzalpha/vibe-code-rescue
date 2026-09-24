# Outreach — siap tempel

Draft final buat 10 target pertama. Tinggal copy-paste pakai akun lu.

**Aturan yang dipatuhi di tiap draft:**
- Nol link, nol harga, nol nama produk. Kalau ada yang nanya "bisa dikerjain?" → itu izinnya, baru tawarin audit.
- **Baris pertama wajib lu sesuaikan** dengan isi post aslinya. Gw cuma punya judul dari hasil search — belum baca postnya (Reddit blokir fetch otomatis). Kalau baris pertama nggak nyambung sama yang dia tulis, **jangan kirim**.
- Satu komentar per thread. Nggak ada bump.

---

## Reddit — prioritas 1

### T1 · r/vibecoding · "Can vibe-coded apps actually survive production?"
`reddit.com/r/vibecoding/comments/1tumgz0`

Dia nanya: di mana app vibe-coded biasanya gagal duluan — security, scaling, deploy, atau maintenance?

```
Deploy, and it's not close. The app logic usually holds up; what breaks is the gap
between "runs in the builder's preview" and "runs against the internet".

Four things, in the order I'd check them:

1. Secrets in the client bundle. Anything prefixed NEXT_PUBLIC_ or VITE_ ships to
   the browser. The builder's preview injects env vars, your host doesn't — so a
   key that was fine in preview is sitting in your production JS.

2. Auth that's only enforced in the UI. Hiding a route behind a client-side check
   is not a check. Every route needs a server-side gate.

3. Row level security, per table. A new table is open by default. Test it with the
   anon key and confirm you get zero rows you don't own.

4. Prod env vs local. Diff the variable names. This is where "works on my machine"
   actually lives, and it fails quietly — the app boots fine and breaks later.

Scaling is usually fine until a few hundred users; these four bite on day one.
```

---

### T2 · r/vibecoding · "Vibe coding kept handing me apps that looked finished but didn't work"
`reddit.com/r/vibecoding/comments/1ulj42l`

Dia sebut: auth yang cuma form, tombol yang nggak ngapa-ngapain, data yang hilang saat refresh.

```
The "looks finished" failure is specific: the happy path got built, the failure
paths didn't. Three checks catch most of it.

Auth that's just a form: does the server actually reject the request when there's
no session? Log out, then hit the route directly with curl. If you get data back,
the form was decoration.

Buttons that do nothing: open devtools, Network tab, click it, and look at the
status code. A 404 or 500 with a success toast on screen is the most common one —
the handler was never wired up.

Data that vanishes on refresh: that's usually state living in the component instead
of the database. If a reload clears it, it was never saved.

All three are visible in an afternoon without reading the whole codebase.
```

---

### T3 · r/vibecoding · "My Lovable app broke at 3am and I had no idea how to fix it"
`reddit.com/r/vibecoding/comments/1so5h1r`

Post-nya sendiri promosi tool lain. Jawab **masalahnya**, jangan tool-nya.

```
The 3am part is the real problem, not the bug. You found out from a user DM.

Before adding a monitoring tool, there's a cheaper first step: make the app tell
you when it breaks instead of failing quietly. Most of these failures are silent —
a webhook returns 500, the payment succeeds at the provider, the order never gets
created, and nothing logs it.

Two things worth checking today:
- Every external call (payments, email, any API) should check the response status
  and throw on failure. Silent failures are usually just an unchecked response.
- Put an error boundary or a global handler somewhere that emails you. It doesn't
  need to be a product.

A checkout flow that crashes loudly is survivable. One that crashes quietly is how
you lose money without knowing.
```

---

### T4 · r/vibecoding · "Your app works, but your code is messy. Now what?"
`reddit.com/r/vibecoding/comments/1s2s15u`

Dia posting checklist pre-scale (query DB, error handling, staging, 10x load). **Tambahkan satu yang dia lewatkan** — jangan jualan.

```
Good list. One thing missing from it, and it's the one that actually costs money:
nothing here checks what's exposed to the browser.

Worth adding as step zero, before the performance work:

Open your production bundle and search the JS for anything key-shaped. Anything
prefixed NEXT_PUBLIC_ / VITE_ / PUBLIC_ is in there. If a database URL, a Stripe
secret, or a service-role key got that prefix, it's public right now — and rotating
it is more urgent than any query optimization.

Same pass: for each table, use the anon key from the browser and try to read rows
you don't own. If you get them, the policy is missing.

Performance debt you can pay down over months. A leaked key is a countdown.
```

---

### T5 · r/Supabase · "Need clarifications on Row Level Security"
`reddit.com/r/Supabase/comments/1ppq2qv`

```
The mental model that makes it click: the anon key is not a secret, and it isn't
supposed to be. It identifies your project. RLS is what decides what that key can
read.

Two access paths, and they behave differently:
- anon/publishable key → goes through RLS. This is what your browser uses.
- service_role key → bypasses RLS entirely. Server-side only, never in the client.

So "is my data exposed" is not answered by looking at the key. It's answered per
table: is RLS enabled, and is there a policy that says who can select?

The test that settles it — in the browser console, with the anon key, try to select
rows you shouldn't own. Zero rows means it's working. Rows back means RLS is off or
the policy is `using (true)`.

New tables are open by default. That's the one that catches everybody.
```

---

### T6 · r/Supabase · "Supabase RLS is not for production"
`reddit.com/r/Supabase/comments/1mvjpr8`

Thread kontroversial, banyak jawaban salah. Jadilah yang benar.

```
Worth separating two different claims that get merged in these threads.

Claim 1: RLS is not a substitute for server-side authorization. True. If your app
has business rules ("only the owner can refund"), those belong in your API, not in
a policy.

Claim 2: therefore you can turn RLS off. That one doesn't follow. Turning it off
means the anon key in your browser can read every row in every table. The policy
isn't your authorization layer — it's the thing standing between a public key and
your whole dataset.

The workable setup is both: RLS on with restrictive policies as the floor, and your
server enforcing the business logic on top. RLS is the seatbelt, not the driver.

If you're using service_role for everything server-side, RLS is irrelevant there —
but it still matters for whatever the browser can reach.
```

---

### T7 · r/Supabase · "service_role API key not bypassing RLS"
`reddit.com/r/Supabase/comments/1crhv56`

```
Check which client you're actually holding. `createClient` with the service key
doesn't bypass RLS by itself — the key has to be the one going into the
Authorization header, and it's easy to end up with a client that's still using the
anon key you passed somewhere else.

Also: service_role bypasses RLS but does not bypass table grants. If the role lost
its grant on that table, you'll get a permission error that looks like a policy
problem.

Quick way to tell them apart — run the query with the service key and look at the
error. "permission denied for table" is grants. Empty result with no error is RLS.
```

---

## X — reply, jangan post

Balasan serbaguna. Sesuaikan baris pertama sama post yang lu balas.

### T8 · Post soal `NEXT_PUBLIC_` bocorin secret

```
That prefix is the whole bug — NEXT_PUBLIC_ / VITE_ / PUBLIC_ all mean "ship this
to the browser". The builder's preview injects env vars, your host doesn't, so the
same var is harmless in dev and public in prod.

Rotate the key today, then move that call behind a server route. The value never
needs to reach the client.
```

### T9 · Post "works locally, breaks in production"

```
Classic env split. Diff the variable names between prod and local first — that
catches most of it. Then confirm the deploy is actually running the new commit and
not a cached build.

Both fail quietly: the app boots fine and breaks on one specific path.
```

### T10 · Post "Stripe says paid but my app doesn't know"

```
That's a webhook that's failing silently. Check the delivery log in the Stripe
dashboard — failed attempts will tell you whether it's the signature secret or the
endpoint not being reachable from outside.

Either way the order never gets created, and nothing on your side throws.
```

### T11 · Post kehilangan signup / form yang nggak ngirim

```
Open devtools → Network → submit it → look at the actual status code, not the
success message.

A 404 on the handler with a "Thanks!" on screen is the most common version of this.
Leads have been disappearing with no error anywhere.
```

---

## Discord — Lovable, Bolt, v0, Supabase → #help

Balasan serbaguna, khusus channel help.

```
Exporting out of the builder is where env vars usually break — the preview injects
them, your host doesn't. Copy the exact names into your host's dashboard and
redeploy; that fixes a large share of "works in preview, not in prod".

If it still misbehaves after that, check two things:
- nothing secret got prefixed NEXT_PUBLIC_ / VITE_ (it ships to the browser)
- RLS is on, per table, tested with the anon key

Happy to look at the repo structure if you paste it.
```

---

## Cara jalanin — 30 menit

1. **Buka T1 di browser** (login dulu). Baca postnya. Kalau baris pertama draft gw nggak nyambung, tulis ulang satu baris itu. Paste sisanya.
2. Ulangi T2 → T7. **Satu komentar per thread, jangan balas lagi.**
3. Kalau ada yang nanya "do you do this for hire?" → **baru** jawab:
   > Yeah — I run a $150 48-hour audit that produces exactly this list with fix
   > costs. Money back if there's nothing serious in it. Happy to start with that.
4. X dan Discord: pakai balasan serbaguna, sesuaikan pembukaannya.

**Yang bikin ini jalan:** T1–T7 semuanya jawaban jujur. Kalau lu nggak dapet klien dari situ pun, reputasi akun lu naik dan itu modal buat posting berikutnya. Jangan lompat ke pitch di thread yang belum kenal lu.
