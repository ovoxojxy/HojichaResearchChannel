#!/usr/bin/env python3
"""
Script to replace "RA3" with "Chris" in messages in the Slack channel.
"""

import os
import urllib.request
import urllib.error
import json
import time

# Configuration
CHANNEL_ID = "C0A6ZJ9NH5E"
USER_TOKEN = os.environ["SLACK_USER_TOKEN"]
JAROD_USER_ID = "U09Q359K49Z"

# Messages to edit (timestamp: new_text)
MESSAGES_TO_EDIT = {
    # Jarod's messages mentioning RA3
    "1767299270.399309": "and Chris i need you to stress test the partial observability",
    "1767299271.213559": "use the same pilot_v0.1 traces and assign a level 0 / 1/ 2",
    "1767299272.053529": "heere we're assuming the conversation history is hidden, tool outputs are sanitized or unavailable and that only tool call sequence, error types, and final outcome are visible",
    "1767149908.445249": """Ok Chris — You'll stress-test the same pilot trajectories under partial observability. You will receive the same 6 trajectories, but assume: - Conversation history is hidden - Tool outputs are sanitized - Only the following are observable: - tool call names + order - error types/messages - final validation outcome (success/failure) Your task: For each trajectory: - Assign a level (0, 1, or 2) if possible - If not possible, say "ambiguous" and explain why - Identify which observable signals were sufficient or insufficient Focus on: - Whether outcome-based indicators alone are diagnostic - Where partial observability breaks or holds Do NOT propose new signals or changes to the rubric. Post results in Slack.""",
    "1767148027.156449": "Ok Chris — We are locking the toy task to the deferred configuration validation setup. Your task: Analyze the toy task under partial observability and deployment constraints. Specifically: - Identify which signals remain observable if conversation history and tool outputs are hidden or sanitized - Explain how outcome-based indicators (task success, error patterns, re-queries, efficiency) remain diagnostic - Clarify what signals fail under partial observability and why that does not break the evaluation - Write this as a deployment-robustness subsection for the paper No redesigns or new signals. Slack response only.",
    "1767147530.812689": "Ok Chris — The retention spec is frozen. Your task: - Validate that the toy task remains diagnostic under partial observability. - Confirm which outcome-based signals remain usable if tool outputs and context are hidden. No new signals or behaviors. Slack response only.",
    "1767288248.064099": "and you Chris can you also give a quick summary of the git repo",
    
    # Also update the message that mentions "we'll rerun RA2 labeling and RA3 partial-observability stress testing"
    "1767321114.048379": """Alex go ahead and implement validate_config_v2 on your branch and generate a small paired set (~20 trajectories).
Once that's ready, we'll rerun Brent labeling and Chris partial-observability stress testing and see what changes.""",
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
    print(f"Starting to edit {len(MESSAGES_TO_EDIT)} messages...")
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

