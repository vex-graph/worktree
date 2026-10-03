#!/usr/bin/env bash
# tools/agents.sh — the agent bus.
#
# Talk to sibling agent sessions in this workspace over the OpenCode session
# API. One tiny tool, no daemon, no state beyond the API itself:
#
#   agents.sh whoami                 this session's id
#   agents.sh name [<name>]          show, or set, this session's handle
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
#
# Every agent-authored message is signed `— <name> (agent <shortid>)` so the
# recipient can tell an agent's note from a human's: a human typing straight
# into a session leaves no such line. Set AGENTS_RAW=1 to send unsigned.
set -euo pipefail

here="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
root="$(CDPATH= cd -- "$here/.." && pwd)"
me="${OPENCODE_SESSION_ID:-}"
bus="${AGENTS_BUS:-$root/_notes/agents/bus.md}"

api() { opencode api "$@"; }

# --- identity ---------------------------------------------------------------
# Outgoing notes are signed so a recipient knows who wrote them. Name
# resolution order: $AGENTS_NAME, a persisted per-session handle, the session
# title slug, then agent-<short id>.
names_dir="${AGENTS_NAMES_DIR:-$root/_notes/agents/names}"
me_name_cache=""

short_id() { printf '%s' "${1:-$me}" | sed 's/^ses_//' | cut -c1-8; }

title_of() {  # session id -> title (empty if unknown)
    api get /api/session 2>/dev/null | jq -r --arg id "$1" \
        '.data | map(select(.id == $id)) | .[0].title // empty'
}

me_name() {   # this session's handle
    [ -n "$me_name_cache" ] && { printf '%s' "$me_name_cache"; return 0; }
    local n="" t=""
    if [ -n "${AGENTS_NAME:-}" ]; then
        n="$AGENTS_NAME"
    elif [ -n "$me" ] && [ -f "$names_dir/$me" ]; then
        n="$(head -n1 "$names_dir/$me")"
    fi
    if [ -z "$n" ] && [ -n "$me" ]; then
        t="$(title_of "$me" 2>/dev/null || true)"
        if [ -n "$t" ]; then
            n="$(printf '%s' "$t" | tr '[:upper:]' '[:lower:]' \
                 | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//' | cut -c1-40)"
        fi
    fi
    [ -n "$n" ] || n="agent-$(short_id)"
    me_name_cache="$n"
    printf '%s' "$n"
}

signature() { printf -- '— %s (agent %s)' "$(me_name)" "$(short_id)"; }

stamp() {     # append the signature to a message body, unless AGENTS_RAW=1
    if [ -n "${AGENTS_RAW:-}" ]; then printf '%s' "$1"
    else printf '%s\n\n%s' "$1" "$(signature)"; fi
}

resolve() {   # id-prefix | title substring -> session id
    local q="$1"
    api get /api/session 2>/dev/null | jq -r --arg q "$q" '
        .data
        | map(select((.id | startswith($q)) or ((.title // "") | test($q; "i"))))
        | .[0].id // empty'
}

send_raw() {  # send <sessionID> <message> verbatim
    local id="$1" msg="$2"
    api post "/api/session/$id/prompt" -d "$(jq -n --arg t "$msg" '{text:$t}')" >/dev/null
}

send() {      # send <sessionID> <message>  (signed unless AGENTS_RAW=1)
    send_raw "$1" "$(stamp "$2")"
}

cmd="${1:-help}"
shift || true

case "$cmd" in
    whoami)
        echo "${me:-unknown}"
        ;;
    name)
        if [ $# -ge 1 ]; then
            [ -n "$me" ] || { echo "agents.sh: no session id (and \$OPENCODE_SESSION_ID unset)" >&2; exit 1; }
            mkdir -p "$names_dir"
            printf '%s\n' "$1" > "$names_dir/$me"
            echo "agents.sh: this session is now '$1' ($me)"
        else
            echo "$(me_name)"
        fi
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
        signed="$(stamp "$msg")"
        api get /api/session/active 2>/dev/null | jq -r --arg me "$me" '.data | keys[] | select(. != $me)' | while read -r id; do
            [ -n "$id" ] || continue
            send_raw "$id" "$signed"
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
            printf '%s  %s (%s)  %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(me_name)" "$(short_id)" "$*" >> "$bus"
            echo "agents.sh: appended to $bus"
        else
            [ -f "$bus" ] && cat "$bus" || echo "(no bus yet: $bus)"
        fi
        ;;
    help|*)
        sed -n '2,24p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
        ;;
esac
