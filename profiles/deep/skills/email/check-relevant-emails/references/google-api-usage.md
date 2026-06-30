# Google Workspace API Usage Notes

## google_api.py CLI Usage

The `google_api.py` script in the Google Workspace skill has a specific interface:

- **Default output is JSON** - The script outputs JSON by default, so flags like `--format json` are not recognized and will cause an error.
- **Correct usage examples:**
  ```bash
  # Search emails (JSON output by default)
  python google_api.py gmail search "in:inbox newer_than:2h" --max 50

  # Get full email by ID
  python google_api.py gmail get MESSAGE_ID

  # List calendar events
  python google_api.py calendar list --max 25
  ```

- **Common mistake to avoid:**
  ```bash
  # THIS WILL FAIL - unrecognized argument --format json
  python google_api.py gmail search "query" --format json
  ```

## Error Messages

When incorrectly adding `--format json`:
```
usage: google_api.py [-h] {gmail,calendar,drive,contacts,sheets,docs} ...
google_api.py: error: unrecognized arguments: --format json
```

This occurs because the script uses argparse and doesn't accept a `--format` flag - JSON output is the default behavior.

## Workflow Implications

For the check-relevant-emails skill:
1. Use `google_api.py gmail search "in:inbox newer_than:2h" --max 50` without any format flags
2. Parse the JSON output directly from stdout
3. Same applies to calendar list and other gws commands

This was discovered during a cron job execution on 2026-05-06 where the skill initially failed due to incorrect flag usage.
