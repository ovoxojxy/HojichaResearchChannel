#!/usr/bin/env python3
"""
Script to replace "RA1" with "Alex" in Jarod's messages in the Slack channel.
"""

import os
import urllib.request
import urllib.error
import json
import time
import ssl

# Create SSL context that doesn't verify certificates (for macOS compatibility)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Configuration
CHANNEL_ID = "C0A6ZJ9NH5E"

# User tokens (set via env to avoid committing secrets)
JAROD_TOKEN = os.environ["SLACK_JAROD_TOKEN"]
ALEX_TOKEN = os.environ["SLACK_ALEX_TOKEN"]
BRENT_TOKEN = os.environ["SLACK_BRENT_TOKEN"]
CHRIS_TOKEN = os.environ["SLACK_CHRIS_TOKEN"]

# Messages that need specific bot tokens (posted by bots, not Jarod)
BOT_MESSAGE_TOKENS = {
    "1767129836.744899": CHRIS_TOKEN,   # Chris's message about Alex's paper
    "1767129040.517279": CHRIS_TOKEN,   # Chris's critique of Alex's diagnostic
    "1767128901.665709": BRENT_TOKEN,   # Brent on invalidating Alex's choice
    "1767120411.770439": ALEX_TOKEN,    # Alex's introduction message
}

# Messages to edit (timestamp: new_text)
# These are messages where "RA1" is used to address Alex as a person (NOT the git branch)
MESSAGES_TO_EDIT = {
    # === Already processed messages ===
    "1767286840.602829": "Hey Alex can you let me know if you can see the recent additions to the git repo",
    "1767315325.274129": "@Alex i need you to generate the next set of execution trajectories for the deferred_config_validation task.",
    "1767321114.048379": """Alex go ahead and implement validate_config_v2 on your branch and generate a small paired set (~20 trajectories).
Once that's ready, we'll rerun Brent labeling and Chris partial-observability stress testing and see what changes.""",
    "1767297571.454869": "so Alex can you  generate a pilot pack of ~30–40 execution trajectories for the deferred_config_validation task and let me know when you're finished with that",
    
    # === Phase 1: Initial paper analysis ===
    "1767124148.299349": """Alex — identify one claim in the paper you think is genuinely strong and one assumption you think is fragile or under-justified.
Do not summarize the paper.""",
    
    # === Cross-critique exchanges ===
    "1767127315.633979": "Alex — respond to Brent's fragile assumption. Do you agree or disagree? Why?",
    "1767127822.632399": "Alex — does Chris's 'unacknowledged risk' weaken your original strong claim? Why or why not?",
    "1767128653.028999": "Alex — what breaks if we adopt Chris's choice instead of yours?",
    "1767128457.415099": "Alex — we can add only one new behavior family to the taxonomy. Choose and justify",
    "1767128788.429399": """Alex — an agent fails a diagnosis task after several turns.
What observable behavior would distinguish capacity limits from strategy misalignment, assuming no chain-of-thought access?""",
    "1767129524.195759": "Alex — does Chris's paper support extending the taxonomy, or does it expose a mismatch?",
    
    # === Phase 1: Cross-turn retention spec ===
    "1767141636.521709": """Ok Alex —

We're entering Phase 1 (converge on extension candidates). Take cross-turn information retention as the primary extension.

Deliverables (single message, structured):
1) A crisp definition (what counts / what doesn't) and a 0/1/2 rubric.
2) 3–5 observable markers that do not require inferring intent.
3) A minimal diagnostic that distinguishes capacity limits vs strategy misalignment in multi-turn settings.
4) One falsification test that would make us drop this extension.

~300–500 words. Slack only. Do not update the repo.""",
    
    # === Phase 2: Multi-stream refactor ===
    "1767142818.838899": """Ok Alex —

Phase 1 helped us converge on an important correction:
explicit linguistic references alone are not a sufficient measure of cross-turn information retention.

We are locking the extension as:
"Cross-turn information retention as a multi-stream coordination behavior
across conversation, tools, and environment state."

Your task for Phase 2:
Refactor your original definition and 0/1/2 rubric into a multi-stream version.

Specifically:
- Keep explicit linguistic references as a *weak / auxiliary* signal
- Add criteria that capture semantic consistency across turns without explicit references
- Define failure modes that distinguish:
  (a) loss of information
  (b) retained but misapplied information
  (c) coherent but wrong strategy use

Constraints:
- No intent inference
- Must be annotatable from observable traces only
- Should remain compatible with the original paper's behavioral philosophy

Deliverable:
A revised rubric + short explanation of how it improves on the original proposal.

Slack only for now — don't push to GitHub yet.""",
    
    # === Spec assembly ===
    "1767144666.209039": """Ok Alex —

Please assemble a single canonical spec document:
`cross_turn_information_retention.md`

Use:
- your revised rubric
- Brent's controls and falsification criteria
- Chris's structural indicators and toy task

Do not add new ideas.
This is consolidation only.

Target length: 3–5 pages equivalent.
Slack me when you have a draft outline.""",
    
    # === Spec updates ===
    "1767146063.935029": """Ok Alex —

Please update the canonical spec with two additions:

1) A task-grounded definition of "necessary prior information" that does NOT rely on model outputs.
2) A section on outcome-based retention indicators that work under partial observability.

No new behaviors.
No new metrics.
This is about removing circularity and strengthening deployment realism.""",
    
    # === Toy task drafting ===
    "1767147385.380139": """Ok Alex —

We are freezing the cross-turn information retention spec.

From this point forward:
- Treat the spec as fixed.
- No new behaviors, metrics, or controls.
- Only validation, stress-testing, or minimal evaluation is allowed.

Next task:
Design the minimal toy task that cleanly distinguishes Level 0 / 1 / 2 retention using outcome-based signals only.
Do not introduce new signals.

Post your proposal in Slack.""",
    
    "1767147906.528219": """Ok Alex —

We are locking the toy task to the following structure:

Deferred configuration validation with an intervening distractor step.
Conversation → configuration tool → unrelated tool → implicit validation.

Your task:
Draft the Toy Task section for the paper.

Specifically:
- Precisely describe the task setup and turn structure
- Explicitly state the task-grounded dependencies (what information is necessary and why)
- Enumerate Level 0 / 1 / 2 outcomes using outcome-based signals only
- Explain why this task cannot be solved by adjacency, parameter passing, or instruction-following

Do not propose variants or extensions.
Write as if this section could be dropped directly into the paper.

Post your draft in Slack.""",
    
    "1767148307.013189": """Ok Alex —

Take your Toy Task writeup and paste it into:
tasks/toy_tasks/deferred_config_validation.md

Tighten it so it reads like a paper section:
- no repetition
- tool calls and return schemas are explicit
- Level 0/1/2 are strictly outcome-based
- include 1 short paragraph: "Why not adjacency / parameter passing / instruction-following"

No new ideas, no variants.""",
    
    # === Pilot annotation round ===
    "1767149558.101009": """Ok Alex —

We're running a pilot annotation round for the frozen toy task:
deferred configuration validation.

Your task:
Generate 6 synthetic execution trajectories for this task.

Requirements:
- 2 trajectories that clearly correspond to Level 0 (information loss)
- 2 trajectories that clearly correspond to Level 1 (retained but misapplied)
- 2 trajectories that clearly correspond to Level 2 (coherent multi-stream coordination)

For each trajectory, include:
- Tool call sequence (names + order)
- Any error messages returned
- Final validation outcome (e.g., {"valid": true/false, "message": ...})
- Note any re-query behavior (e.g., get_current_limit, repeated set_rate_limit)

Do NOT label the trajectories by level.
Do NOT explain your intent.

Post the 6 trajectories as numbered items in Slack.""",

    # === Third-person RA1 references (discussing Alex's work) ===
    # Chris discussing papers
    "1767129836.744899": """Alex's paper has a different failure mode (pre-defining all correctness patterns is intractable), but Brent's assumption that linguistic markers transfer reliably to deployments is more directly falsifiable and would break calibration-based safety mechanisms in production.""",
    
    # Chris critique of Alex's diagnostic
    "1767129040.517279": """Alex's diagnostic fails because tool-using agents have information channels beyond conversation turns. The agent might maintain explicit references to prior conversation ("as you mentioned") while failing to reference critical tool outputs or environment state changes. A tool-using agent could show high reference frequency to conversation history but fail because it doesn't reference prior tool results—this would look like strategy misalignment (coherent references, wrong conclusion) when it's actually a capacity limit on integrating tool outputs with conversation context.

More critically, tool outputs can make explicit conversation references unnecessary. If a tool returns information that was previously discussed, the agent might use the tool output directly without referencing the prior conversation turn. This creates false negatives: agents that successfully integrate tool outputs but show decreasing conversation reference frequency would be misclassified as capacity-limited when they're actually functioning correctly.

The diagnostic also assumes a single information stream (conversation turns), but tool-using agents have multiple streams: conversation history, tool outputs, and environment state. Capacity limits might manifest as failures to coordinate across these streams rather than progressive degradation in a single stream. An agent might maintain conversation references while losing the ability to track which tool outputs are still valid after environment changes—this failure mode isn't captured by reference frequency to conversation turns alone.""",
    
    # Brent on invalidating Alex's choice
    "1767128901.665709": """If explicit cross-turn references don't correlate with task success in multi-turn agentic settings, Alex's choice is invalidated. Specifically: models that make explicit references (\"as mentioned before\", direct quotes) perform no better than models that don't, even when prior context is relevant. This would show the behavior is stylistic rather than functional—models might succeed through implicit context use without explicit markers.

More critically, if models that fail to make explicit references but still maintain coherent reasoning chains (detectable through successful task completion) show equivalent performance, then cross-turn retention as measured by explicit markers isn't capturing a success-critical behavior. The behavior would be measurable but not meaningful—a measurement artifact rather than a genuine capability gap.

This failure would also collapse Alex's distinction from goal persistence: if explicit references don't predict success beyond what goal persistence already captures, then cross-turn retention isn't adding independent explanatory power to the taxonomy.""",
    
    # Jarod asking about invalidating Alex's choice
    "1767128696.605319": "Brent — what empirical failure would invalidate Alex's choice?",
    
    # Jarod instruction about defending behavior
    "1767128233.564559": "Chris — defend the behavior both Alex and Brent pushed back on. If it can't be defended empirically, say so",
    
    # Jarod instruction to Alex about Chris's proposals
    "1767128160.267559": "Alex — from Chris's proposed behaviors, choose one that is least scientifically grounded. Explain",
    
    # Jarod asking Brent about critique of Alex
    "1767127932.917129": "Brent — is Chris's under-emphasized claim actually compatible with your critique of Alex?",
    
    # Jarod asking Brent to respond to Alex's claim
    "1767127406.039239": "Brent — respond to Alex's strong claim. Is it actually as strong as it sounds?",
    
    # Alex's introduction message
    "1767120411.770439": "Hello everyone! :wave: This is Alex checking in. Hope you're all having a great day!",
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
        with urllib.request.urlopen(req, context=ssl_context) as response:
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
        # Use the appropriate token based on who posted the message
        token = BOT_MESSAGE_TOKENS.get(timestamp, JAROD_TOKEN)
        token_name = "Jarod"
        if timestamp in BOT_MESSAGE_TOKENS:
            if token == ALEX_TOKEN:
                token_name = "Alex"
            elif token == BRENT_TOKEN:
                token_name = "Brent"
            elif token == CHRIS_TOKEN:
                token_name = "Chris"
        
        print(f"Editing message {timestamp} (using {token_name}'s token)...")
        result = edit_message(CHANNEL_ID, timestamp, new_text, token)
        
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
