# Backup and Restore Guide

This project includes a simple script to back up configuration files and any
persistent data/cache.

## Scheduled Backups

1. Adjust the directories to back up by setting the `BACKUP_TARGETS`
   environment variable (defaults to `app/config app/data/cache`).
2. Set remote storage credentials:
   - `S3_BUCKET` for uploading to Amazon S3, **or**
   - `REMOTE_HOST` and optional `REMOTE_PATH` for `scp`/`ssh` targets.
3. Schedule the backup script with `cron`:

   ```cron
   0 3 * * * /path/to/repo/scripts/backup.sh >> /var/log/dataprofusion_backup.log 2>&1
   ```

   The above example runs the backup every night at 3 AM.

## Restore Procedure

1. Retrieve the desired archive from your remote storage, e.g.:

   ```bash
   aws s3 cp s3://$S3_BUCKET/dataprofusion-<timestamp>.tar.gz .
   # or
   scp user@host:/path/dataprofusion-<timestamp>.tar.gz .
   ```
2. Extract the archive in the project directory:

   ```bash
   tar xzf dataprofusion-<timestamp>.tar.gz -C /path/to/repo
   ```
3. Restart services that rely on the restored files, if necessary.

## Testing Restores

Regularly verify that backups can be restored by performing a test restore to a
separate environment:

1. Run the backup script manually and restore the archive to a temporary
   location.
2. Execute the unit tests to confirm the application still functions:

   ```bash
   python run_tests.py unit
   ```
3. Discard the temporary environment after verification.

Testing restores periodically ensures the backup process remains reliable and
that the documentation stays current.
