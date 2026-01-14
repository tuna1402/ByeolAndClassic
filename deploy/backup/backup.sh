#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
BACKUP_DIR=${BACKUP_DIR:-"$HOME/backups/byeolandclassic"}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TARGET_DIR="$BACKUP_DIR/$TIMESTAMP"

mkdir -p "$TARGET_DIR"

if [ -f "$REPO_ROOT/db.sqlite3" ]; then
  cp "$REPO_ROOT/db.sqlite3" "$TARGET_DIR/db.sqlite3"
fi

if [ -d "$REPO_ROOT/media" ]; then
  rsync -a "$REPO_ROOT/media/" "$TARGET_DIR/media/"
fi

echo "Backup completed: $TARGET_DIR"
