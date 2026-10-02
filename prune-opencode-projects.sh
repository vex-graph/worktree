#!/usr/bin/env bash
#
# prune-opencode-projects.sh
#
# Deletes every OpenCode project EXCEPT:
#   - fa9669c197e305a9c11a775a8c91202884b46a7a  (/Users/vexgraph/vexgraph)  <- current
#   - global                                    (built-in default project)
#
# OpenCode stores all projects/sessions/messages in one SQLite database.
# There is no CLI/API to delete a project, so this edits the DB directly.
#
# It uses PRAGMA foreign_keys=ON before the DELETE so that the documented
# ON DELETE CASCADE chains fire:
#   project -> session / session_v2 / project_directory / permission / worktree
#   session -> message -> part / todo
#   session_v2 -> session_message / session_inbox / session_pending
#
# Safety:
#   * stops the background service first (required: it is the only writer)
#   * backs up the DB before touching it
#   * runs inside a transaction; aborts on any assertion failure
#   * VACUUM only if the integrity check passes
#
# This script does NOT delete itself and does NOT touch the current project.

set -euo pipefail

DATA_DIR="$HOME/.local/share/opencode"
DB="$DATA_DIR/opencode.db"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$DATA_DIR/backups"
BACKUP="$BACKUP_DIR/opencode.db.$STAMP.bak"

KEEP_FA9669="fa9669c197e305a9c11a775a8c91202884b46a7a"
KEEP_GLOBAL="global"

say()  { printf '\033[1;36m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[warn]\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31m[ERROR]\033[0m %s\n' "$*" >&2; exit 1; }

[ -f "$DB" ] || die "Database not found at $DB"

command -v sqlite3 >/dev/null 2>&1 || die "sqlite3 not found in PATH"
command -v opencode >/dev/null 2>&1 || warn "opencode not found in PATH; skipping service stop/start"

say "Data dir: $DATA_DIR"
say "Database: $DB ($(du -h "$DB" | cut -f1))"

# ---------------------------------------------------------------------------
# 1. Stop the background service (single writer) so the DB is not in use.
# ---------------------------------------------------------------------------
if command -v opencode >/dev/null 2>&1; then
  say "Stopping OpenCode background service"
  opencode service stop >/dev/null 2>&1 || warn "service stop reported an error (may already be stopped)"
fi

# ---------------------------------------------------------------------------
# 2. Back up the database (plus any WAL/SHM).
# ---------------------------------------------------------------------------
mkdir -p "$BACKUP_DIR"
say "Backing up to $BACKUP"
cp "$DB" "$BACKUP"
for ext in -wal -shm; do
  [ -f "$DB$ext" ] && cp "$DB$ext" "$BACKUP$ext"
done
say "Backup complete"

# ---------------------------------------------------------------------------
# 3. Show what will be deleted.
# ---------------------------------------------------------------------------
say "Projects currently tracked:"
sqlite3 -readonly -header -column "$DB" \
  "SELECT substr(id,1,12) AS id, worktree FROM project ORDER BY worktree;"

say "Projects to be DELETED (everything except $KEEP_FA9669 and $KEEP_GLOBAL):"
sqlite3 -readonly -header -column "$DB" \
  "SELECT substr(id,1,12) AS id, worktree
     FROM project
    WHERE id NOT IN ('$KEEP_FA9669','$KEEP_GLOBAL')
    ORDER BY worktree;"

# Build the id list for filesystem cleanup + deletion.
DEL_IDS="$(sqlite3 -readonly "$DB" \
  "SELECT id FROM project WHERE id NOT IN ('$KEEP_FA9669','$KEEP_GLOBAL');")"

if [ -z "$DEL_IDS" ]; then
  say "Nothing to delete. Exiting."
  command -v opencode >/dev/null 2>&1 && opencode service start >/dev/null 2>&1 || true
  exit 0
fi

# ---------------------------------------------------------------------------
# 4. Delete project rows inside a transaction with foreign_keys ON.
#    Assertions guarantee the current project is untouched.
# ---------------------------------------------------------------------------
say "Deleting project rows (cascade) ..."
sqlite3 "$DB" <<SQL
PRAGMA foreign_keys = ON;
BEGIN IMMEDIATE;

-- Guard: refuse to run if the project we must keep is missing.
SELECT CASE
  WHEN (SELECT count(*) FROM project WHERE id='$KEEP_FA9669') <> 1
  THEN RAISE(ABORT, 'current project $KEEP_FA9669 not found; aborting')
END;

DELETE FROM project WHERE id NOT IN ('$KEEP_FA9669','$KEEP_GLOBAL');

-- Guard: current project must still exist.
SELECT CASE
  WHEN (SELECT count(*) FROM project WHERE id='$KEEP_FA9669') <> 1
  THEN RAISE(ABORT, 'current project vanished during delete; rolling back')
END;

COMMIT;
SQL

# ---------------------------------------------------------------------------
# 5. Integrity check, then VACUUM to actually reclaim disk space.
#    (Only accumulated WAL space can be recovered, so VACUUM is optional
#     but recommended.)
# ---------------------------------------------------------------------------
say "Running integrity check"
CHECK="$(sqlite3 -readonly "$DB" "PRAGMA integrity_check;" | head -1)"
if [ "$CHECK" = "ok" ]; then
  say "Integrity check OK. Running VACUUM (this rewrites the whole DB, may take a while) ..."
  sqlite3 "$DB" "PRAGMA foreign_keys = ON; VACUUM;"
  say "VACUUM complete"
else
  warn "Integrity check returned: $CHECK"
  warn "Skipping VACUUM. Restore from $BACKUP if anything looks wrong."
fi

say "Database size now: $(du -h "$DB" | cut -f1)"

# ---------------------------------------------------------------------------
# 6. Remove leftover filesystem state for deleted projects.
# ---------------------------------------------------------------------------
say "Removing matching snapshot/shell directories ..."
for id in $DEL_IDS; do
  for sub in snapshot shell; do
    if [ -d "$DATA_DIR/$sub/$id" ]; then
      rm -rf "$DATA_DIR/$sub/$id"
      echo "    removed $sub/$id"
    fi
  done
done

say "Remaining projects:"
sqlite3 -readonly -header -column "$DB" \
  "SELECT substr(id,1,12) AS id, worktree FROM project ORDER BY worktree;"

# ---------------------------------------------------------------------------
# 7. Restart the service.
# ---------------------------------------------------------------------------
if command -v opencode >/dev/null 2>&1; then
  say "Restarting OpenCode background service"
  opencode service start >/dev/null 2>&1 || warn "service start failed; run 'opencode service start' manually"
fi

say "Done."
say "Backup kept at: $BACKUP"
echo
echo "To restore if needed:"
echo "  opencode service stop"
echo "  cp \"$BACKUP\" \"$DB\""
echo "  rm -f \"$DB\"-wal \"$DB\"-shm"
echo "  opencode service start"
