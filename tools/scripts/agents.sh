#!/usr/bin/env bash
here="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec "$here/../shell/agents.sh" "$@"
