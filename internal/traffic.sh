#!/bin/sh
# Who is actually visiting rescue.soyuz.my.id.
#
# The container's nginx logs to stdout, and its log_format appends
# $http_x_forwarded_for — so the REAL client IP survives cloudflared.
# This reads those logs and separates humans from bots and from your own checks.
#
#   sh internal/traffic.sh          # all time
#   sh internal/traffic.sh 500      # last 500 request lines
#   SELF="1.2.3.4 5.6.7.8" sh internal/traffic.sh   # drop your own IPs
#
# ponytail: reads docker logs, so history dies when the container is recreated.
# Move to Cloudflare Web Analytics when you want it to persist.
set -e
N="${1:-0}"

# Access-log lines only: they start with the client IP. Error-log lines also
# contain `request: "GET ..."` but end with `host: "..."`, which corrupts the parse.
RAW=$(docker logs vibe-rescue 2>&1 | grep -E '^[0-9a-f.:]+ - - \[')
[ "$N" -gt 0 ] && RAW=$(printf '%s\n' "$RAW" | tail -n "$N")

printf '%s\n' "$RAW" | awk -v self="$SELF" '
  # log_format: ip - - [date time] "REQ" status bytes "ref" "ua" "xff"
  # UA strings contain spaces, and the line ends with a trailing space, so grab
  # the last two quoted fields in one match and split them on the quote gap.
  {
    ip=$1; status=$9
    match($0, /"[^"]*" "[^"]*"$/)
    tail=substr($0, RSTART, RLENGTH)
    split(tail, f, "\" \"")
    ua=substr(f[1], 2)
    xff=substr(f[2], 1, length(f[2])-1)
    match($0, /"(GET|POST|HEAD) [^ ]+/)
    path=substr($0, RSTART+1, RLENGTH-1); sub(/^(GET|POST|HEAD) /, "", path); sub(/\?.*/, "", path)

    real = (xff == "" || xff == "-") ? ip : xff

    # mawk has no /i flag — lowercase first.
    lua = tolower(ua)
    if (lua ~ /curl|python|wget|bot|crawler|spider|facebookexternalhit|slackbot|whatsapp|headlesschrome|lighthouse|monitor|uptime|preview|scan/) { nbot++; next }
    split(self, s, " ")
    for (i in s) if (s[i] != "" && real == s[i]) { nself++; next }

    total++
    ips[real]++
    paths[path]++
    if (ua ~ /iPhone|Android|Mobile/) dev["mobile"]++
    else if (ua ~ /Mozilla/) dev["desktop"]++
    else dev["other"]++
    if (match($0, /"https?:\/\/[^"]+"/)) refs[substr($0, RSTART+1, RLENGTH-2)]++
  }
  END {
    printf "\n=== real visitors (bots, curl, link previews excluded) ===\n"
    printf "requests: %d   excluded: %d bot, %d self\n\n", total, nbot, nself

    printf "distinct visitors:\n"
    for (i in ips) printf "  %-16s %d\n", i, ips[i]

    printf "\ndevice:\n"
    for (d in dev) printf "  %-8s %d\n", d, dev[d]

    printf "\npages:\n"
    for (p in paths) printf "  %-28s %d\n", p, paths[p]

    printf "\nreferrers:\n"
    n=0; for (r in refs) { printf "  %s (%d)\n", r, refs[r]; n++ }
    if (n == 0) printf "  (none — all direct)\n"
  }
'
