#!/usr/bin/env python3
"""
Script to replace remaining instances of "RA2" with "Brent" in all messages in the Slack channel.
This includes messages from any user that mention RA2.
"""

import os
import urllib.request
import urllib.error
import json
import time

# Configuration
CHANNEL_ID = "C0A6ZJ9NH5E"
USER_TOKEN = os.environ["SLACK_USER_TOKEN"]

# Additional messages to edit (from Alex and others mentioning RA2)
MESSAGES_TO_EDIT = {
    # Jarod's message about rerunning RA2 labeling
    "1767321114.048379": """Alex go ahead and implement validate_config_v2 on your branch and generate a small paired set (~20 trajectories).
Once that's ready, we'll rerun Brent labeling and RA3 partial-observability stress testing and see what changes.""",
    
    # Alex's message about being ready for RA2 labeling
    "1767321328.119619": "Ready to label. I'll go through the pilot_v0.2_paired traces and see if the structured error info resolves the ambiguity issues I flagged in pilot_v0.2.",
    
    # Alex's response about RA2 proposal
    "1767320856.982599": """@Jarod — does this tool addition make sense to you?
It's minimal, backward-compatible, and directly motivated by the ambiguity we've been seeing.
If you're good with it, I'll implement + generate a small pilot pack.""",
}


def edit_message(channel_id, timestamp, text, user_token):
    """Edit a Slack message using the chat.update API."""
    url = "https://slack.com/api/chat.update"
    headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "channel": channel_id,
        "ts": timestamp,
        "text": text,
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.reason}"}


def main():
    """Main function to edit all messages."""
    print(f"Starting to edit {len(MESSAGES_TO_EDIT)} additional messages...")
    print()
    
    success_count = 0
    error_count = 0
    
    for timestamp, new_text in MESSAGES_TO_EDIT.items():
        print(f"Editing message {timestamp}...")
        result = edit_message(CHANNEL_ID, timestamp, new_text, USER_TOKEN)
        
        if result.get("ok"):
            print(f"  ✓ Successfully edited message {timestamp}")
            success_count += 1
        else:
            print(f"  ✗ Failed to edit message {timestamp}")
            print(f"    Error: {result.get('error', 'Unknown error')}")
            error_count += 1
        
        # Rate limiting - be nice to the API
        time.sleep(1)
    
    print()
    print("=" * 60)
    print(f"Summary:")
    print(f"  Successfully edited: {success_count}")
    print(f"  Failed: {error_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()

