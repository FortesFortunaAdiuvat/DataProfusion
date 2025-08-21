#!/bin/bash
set -euo pipefail

# Directories to include in the backup. Override with BACKUP_TARGETS env var.
TARGETS=${BACKUP_TARGETS:-"app/config app/data/cache"}

TIMESTAMP=$(date +"%Y%m%d%H%M%S")
ARCHIVE="dataprofusion-${TIMESTAMP}.tar.gz"

# Create archive; ignore directories that may not exist.
tar czf "$ARCHIVE" $TARGETS --ignore-failed-read

# Upload to remote storage when configured.
if [[ -n "${S3_BUCKET:-}" ]]; then
    aws s3 cp "$ARCHIVE" "s3://${S3_BUCKET}/"
    rm "$ARCHIVE"
elif [[ -n "${REMOTE_HOST:-}" ]]; then
    scp "$ARCHIVE" "${REMOTE_HOST}:${REMOTE_PATH:-.}/"
    rm "$ARCHIVE"
else
    echo "Backup created at $PWD/$ARCHIVE"
fi
