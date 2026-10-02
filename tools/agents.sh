#!/usr/bin/env bash
# tools/agents.sh — the agent bus.
#
# Talk to sibling agent sessions in this workspace over the OpenCode session
# API. One tiny tool, no daemon, no state beyond the API itself:
#
#   agents.sh whoami                 this session's id
#   agents.sh peers                  list sessions (running first)
#   agents.sh running                ids of running sessions
#   agents.sh say <id|title> <msg>   send a message to one session
#   agents.sh tell <msg>             send to every OTHER running session
#   agents.sh inbox [id]             read a session's inbox
#   agents.sh log [id] [n]           read a session's last n messages
#   agents.sh bus [msg]              show, or append to, the shared bus file
#
# A message lands in the target session as a user turn (Session.Inbox.User); a
# running agent picks it up on its next turn. Announce scope before touching a
# shared path, and check `peers` when you are about to edit a file another
# session may own.
set -euo pipefail

here="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
root="$(CDPATH= cd -- "$here/.." && pwd)"
me="${OPENCODE_SESSION_ID:-}"
bus="${AGENTS_BUS:-$root/_notes/agents/bus.md}"

api() { opencode api "$@"; }

resolve() {   # id-prefix | title substring -> session id
    local q="$1"
    api get /api/session 2>/dev/null | jq -r --arg q "$q" '
        .data
        | map(select((.id | startswith($q)) or ((.title // "") | test($q; "i"))))
        | .[0].id // empty'
}

send() {      # send <sessionID> <message>
    local id="$1" msg="$2"
    api post "/api/session/$id/prompt" -d "$(jq -n --arg t "$msg" '{text:$t}')" >/dev/null
}

cmd="${1:-help}"
shift || true

case "$cmd" in
    whoami)
        echo "${me:-unknown}"
        ;;
    peers)
        api get /api/session 2>/dev/null | jq -r --arg me "$me" '
            .data
            | sort_by(.time.updated) | reverse
            | .[]
            | "\(if .id == $me then "*" else " " end) \(.id)  \((.outcome // "?") | .[0:9])  \((.title // "")[0:64])"'
        ;;
    running)
        api get /api/session/active 2>/dev/null | jq -r --arg me "$me" '.data | keys[] | select(. != $me)'
        ;;
    say)
        id="$(resolve "${1:?usage: agents.sh say <id|title> <message>}")"
        msg="${2:?usage: agents.sh say <id|title> <message>}"
        [ -n "$id" ] || { echo "agents.sh: no session matches '$1'" >&2; exit 1; }
        send "$id" "$msg"
        echo "agents.sh: sent to $id"
        ;;
    tell)
        msg="${1:?usage: agents.sh tell <message>}"
        api get /api/session/active 2>/dev/null | jq -r --arg me "$me" '.data | keys[] | select(. != $me)' | while read -r id; do
            [ -n "$id" ] || continue
            send "$id" "$msg"
            echo "agents.sh: sent to $id"
        done
        ;;
    inbox)
        id="${1:-$me}"
        [ -n "$id" ] || { echo "agents.sh: no session id (and \$OPENCODE_SESSION_ID unset)" >&2; exit 1; }
        api get "/api/session/$(resolve "$id" 2>/dev/null || echo "$id")/inbox" 2>/dev/null | jq '.data'
        ;;
    log)
        id="$(resolve "${1:?usage: agents.sh log <id|title> [n]}")"
        n="${2:-6}"
        [ -n "$id" ] || { echo "agents.sh: no session matches '$1'" >&2; exit 1; }
        api get "/api/session/$id/message" 2>/dev/null | jq -r --argjson n "$n" '
            .data[-$n:][]
            | .type as $t
            | [$t, ([.content[]? | select(.type == "text") | .text] | join(" "))]
            | @tsv' | cut -c1-220
        ;;
    bus)
        if [ $# -ge 1 ]; then
            mkdir -p "$(dirname "$bus")"
            printf '%s  %s  %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${me:-?}" "$*" >> "$bus"
            echo "agents.sh: appended to $bus"
        else
            [ -f "$bus" ] && cat "$bus" || echo "(no bus yet: $bus)"
        fi
        ;;
    help|*)
        sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
        ;;
esac
