# Audit Checklist 48 Jam — Vibe Code Rescue

Dokumen **internal**. Dipakai waktu ngerjain audit $150. Tujuannya: dalam 48 jam
klien dapet laporan yang isinya bukti, bukan opini — dan laporan itu bikin dia
ngerti kenapa lanjut ke Rescue Fix worth it.

**Aturan keras:**
- Tiap temuan wajib ada **bukti**: output terminal, status code, screenshot, atau potongan file. Nggak ada temuan tanpa bukti. Kalau nggak bisa dibuktikan, tulis di bagian "perlu dicek lebih lanjut", bukan di daftar temuan.
- Audit itu **read-only**. Jangan ubah kode, jangan deploy, jangan hapus apa pun. Kalau nemu secret yang bocor, lapor + sarankan rotate — jangan rotate sendiri.
- Jangan nulis severity berdasarkan feeling. Pakai tabel severity di bawah.
- Akses klien dicabut begitu kerjaan selesai. Secret yang ketemu **jangan disimpan di mana pun** di luar laporan.

---

## Tabel severity

| Severity | Artinya | Contoh |
|---|---|---|
| **Critical** | Data atau uang bisa bocor/ilang sekarang, tanpa usaha khusus | Service-role key di bundle, RLS mati di tabel user, endpoint admin tanpa auth |
| **High** | Bocor kalau ada yang sengaja nyari; fitur inti rusak | anon key + policy permissive, form utama gagal kirim, webhook Stripe nggak jalan |
| **Medium** | Fitur nggak jalan sebagian, atau risiko kalau di-scale | env var prod salah, DNS/redirect salah, error nggak ke-log |
| **Low** | Kebersihan, performa, potensi masalah ke depan | dependency usang, header keamanan kurang, build warning |

Urutan pengerjaan di bawah = urutan **temuan tercepat per menit**. Kerjain urut,
jangan lompat. Berhenti dan catat begitu ketemu bukti, lanjut ke item berikutnya.

---

## 1. API key bocor di bundle / page source (30–60 menit)

**Yang dicek:** secret yang ikut ke-ship ke browser. Ini paling cepat nemu temuan
dan paling mahal kalau kelewat.

**Cara:**
```bash
# 1. Ambil bundle produksi
curl -sL https://<domain>/ | grep -oE '/_next/static/[^"]+\.js' | head

# 2. Download semua JS, cari pola key
curl -sL https://<domain>/ > /tmp/page.html
grep -rEo 'sk-[A-Za-z0-9_-]{16,}|sk_live_[A-Za-z0-9]{16,}|AIza[0-9A-Za-z_-]{20,}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}|SUPABASE_SERVICE|service_role' /tmp/page.html

# 3. Di repo: cari pemakaian di kode client
grep -rnE 'NEXT_PUBLIC_|VITE_|PUBLIC_' --include='*.ts*' --include='*.js*' .
grep -rnE 'SUPABASE_SERVICE_ROLE|SERVICE_ROLE_KEY|sk_live|STRIPE_SECRET' .
```
Cek juga: `.env` yang ke-commit, `next.config` yang nge-inline env, source map
yang ke-publish (`/…/main.js.map` masih bisa diakses?).

**Contoh temuan:**
> `NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY` dipakai di `lib/supabase.ts` dan ikut
> ke bundle `/_next/static/chunks/main-8f2a.js`. Siapa pun bisa ambil key itu dan
> baca/tulis seluruh database. **Severity: Critical.**

**Fix estimate:** rotate key + pindah call ke server route → 2–4 jam.
Kalau udah ke-publish lama: tambah 1 jam buat cek abuse log.

---

## 2. Auth & Row Level Security (1–2 jam)

**Yang dicek:** apakah batas akses beneran ada, atau cuma kelihatan ada.

**Cara:**
```bash
# RLS status tiap tabel (pakai anon key dari browser, BUKAN service key)
curl -s "https://<proj>.supabase.co/rest/v1/<table>?select=*&limit=5" \
  -H "apikey: <ANON_KEY>" -H "Authorization: Bearer <ANON_KEY>"
# Harus balik [] atau error policy — kalau balik data orang lain: RLS mati
```
Di repo: cari `create policy`, `enable row level security`, dan endpoint API yang
nggak ngecek session. Cek juga middleware auth: apakah route dilindungi di server
atau cuma di client (client-only guard = nggak ada guard).
Test langsung: login sebagai user A, coba akses resource user B lewat URL/API.

**Contoh temuan:**
> Tabel `orders` RLS off. Request pakai anon key balik 5 order milik user lain
> (output curl terlampir). **Severity: Critical.**

**Fix estimate:** policy per tabel + test anon key → 3–6 jam, tergantung jumlah tabel.

---

## 3. Env var & konfigurasi produksi (1 jam)

**Yang dicek:** prod ≠ local. Ini penyebab paling umum "jalan di laptop doang".

**Cara:**
```bash
# Daftar nama env yang dipakai di kode vs yang ada di host/dashboard
grep -rhoE 'process\.env\.[A-Z_0-9]+' --include='*.ts*' --include='*.js*' . | sort -u
# Bandingkan manual dengan env di Vercel/Netlify/host lain. Cek yang kosong/typo/ketuker.
```
Cek juga: `.env.example` yang nggak sinkron, var yang ke-set di preview tapi nggak
di production, dan nilai yang masih pakai default dev.

**Contoh temuan:**
> `DATABASE_URL` ada di preview, nggak ada di production. Build lolos, runtime
> gagal waktu ada request pertama. **Severity: Medium.**

**Fix estimate:** set var + redeploy + verifikasi → 1–2 jam.

---

## 4. Deploy & DNS (1 jam)

**Yang dicek:** apa yang beneran jalan di domain itu, dan apakah itu commit terbaru.

**Cara:**
```bash
dig +short <domain>            # A / CNAME — nunjuk ke mana?
curl -sI https://<domain> | head -20   # header, redirect chain, WWW vs non-WWW
curl -sI https://www.<domain> | head -5
```
Cek: build terakhir di dashboard vs commit terakhir di repo (stale build?),
redirect loop, SSL/expiry, `www` dan root yang nunjuk ke dua tempat beda,
dan env di deploy yang ketinggalan.

**Contoh temuan:**
> `www` → Vercel, root → VPS lama. Dua versi app jalan bareng; user dapat versi
> lama kalau ngetik tanpa `www`. **Severity: Medium.**

**Fix estimate:** perbaiki DNS/redirect + hapus deploy lama → 1 jam.

---

## 5. Form (1 jam)

**Yang dicek:** form yang kelihatan sukses tapi nggak ngirim apa-apa.

**Cara:** submit form di devtools → Network → lihat **status code asli**, bukan
pesan sukses di UI. Cek juga handler-nya ada nggak, dan tulisannya masuk ke tabel
beneran nggak. Coba juga kirim data kosong/invalid — ada validasi server atau cuma
client?

**Contoh temuan:**
> Form kontak POST ke `/api/contact`, balik **404** (handler nggak pernah dibuat).
> UI nampilin "Terima kasih!" tetap. Semua lead hilang sejak launch.
> **Severity: High.**

**Fix estimate:** bikin handler + validasi server + test → 2–3 jam.

---

## 6. Integrasi (2–3 jam)

**Yang dicek:** Stripe, webhook, dan API pihak ketiga yang gagal **diam-diam**.

**Cara:**
- Stripe: cek webhook delivery log di dashboard — ada `failed`? Signature secret cocok?
- Webhook lokal: cek endpoint bisa diakses dari luar (bukan `localhost`), balik 2xx?
- API luar: cari `catch {}` kosong dan `res.ok` yang nggak pernah dicek.
```bash
grep -rnE 'catch\s*\([^)]*\)\s*\{\s*\}|\.then\([^)]*\)\s*\.catch\(\(\)\s*=>\s*\{\s*\}\)' --include='*.ts*' --include='*.js*' .
```
**Contoh temuan:**
> Webhook Stripe balik 500 karena signature secret beda antara prod dan Stripe.
> Stripe retry 3 hari lalu nyerah. 12 pembayaran sukses di Stripe, 0 order kebuat
> di app. **Severity: High.**

**Fix estimate:** benerin secret + replay event yang gagal + bikin log → 3–5 jam.

---

## Template laporan klien

> Klien-facing → **English**. Bagian internal di atas tetap Indonesia.

```
# Audit Report — <client app>
Prepared by Asep · <date> · Read-only audit, no changes made

## Executive summary
<2–4 sentences: how many findings, which one matters most, what it is costing
them right now. No jargon. If the app is safe to use while fixes are scheduled,
say so; if it is not, say that first.>

## Findings

### F-1 — <short title>
Severity: Critical | High | Medium | Low
Where:  <file / table / URL>
Evidence:
  <exact command + output, status code, or screenshot reference>
Impact:  <what breaks or leaks, in money or data terms>
Fix:     <what has to change>
Estimate: <hours> → <$range>

### F-2 — ...
(repeat)

## Fix cost estimate
| Finding | Severity | Estimate |
|---|---|---|
| F-1 | Critical | 4 h — $200 |
| ... | | |
Total: <hours> — <$range>

## Recommendation
<What to fix first and why. Say plainly if something does NOT need fixing —
it builds trust and it is honest. Offer the Rescue Fix and the retainer, but
only for the work that is actually needed.>

## What I did not check
<Anything out of scope or blocked by missing access. Never leave this blank —
an empty scope note reads as a claim of completeness you cannot back up.>
```

**Sebelum kirim, cek ulang:**
- [ ] Tiap temuan ada buktinya, bisa dibuka klien sendiri.
- [ ] Nggak ada klaim yang nggak bisa gue pertanggungjawabkan.
- [ ] Nggak ada secret lengkap di dalam laporan — tunjukin lokasinya + 4 karakter pertama, sisanya sensor.
- [ ] Estimasi jam realistis, ada buffer.
- [ ] Bahasa Inggrisnya sederhana; klien bukan selalu developer.
