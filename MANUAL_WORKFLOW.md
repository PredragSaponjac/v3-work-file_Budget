# ORCA V3 Budget — Manual Workflow (Zero API Cost)

## Schedule: Mon-Fri at 9:30 AM, 1:00 PM, 3:00 PM CT

You will receive a Telegram reminder at each time with exact instructions.

---

## Step 1: Catalyst Hunt (3 models independently)

Open `prompts/r1_master_v5_3.txt` — this is your R1 prompt.

Paste it into ALL THREE AI desktops:
1. **Claude desktop** → paste prompt → send → save output as `claude_ideas.txt`
2. **ChatGPT** → paste prompt → send → save output as `gpt_ideas.txt`
3. **Gemini** → paste prompt → send → save output as `gemini_ideas.txt`

Each AI hunts catalyst ideas independently using its own knowledge + browsing.
No input data needed — the prompt is self-contained.

Save all 3 files to: `C:\Users\18329\Downloads\v3-work-file_Budget\orca_results\`

## Step 2: Consensus

Bring the 3 outputs back to Claude Code:
```
python consensus.py claude_ideas.txt gpt_ideas.txt gemini_ideas.txt
```

This merges the best ideas from all 3 models.

## Step 3: Publish

```
python publish.py consensus_output.txt
```

Sends to Telegram + X.

---

## Key Files
| File | Purpose |
|---|---|
| `prompts/r1_master_v5_3.txt` | R1 catalyst hunter prompt (paste into AI desktops) |
| `prompts/catalyst_confirmation_v2.txt` | Confirmation prompt (optional Stage 2) |
| `prompts/flow_module_v5_7.txt` | UW flow analysis prompt |
| `prompts/methodology_note.txt` | Methodology context |

## What NOT to do
- Do NOT run `pipeline_v20.py` — it calls paid APIs
- Do NOT enable the old scheduled tasks — they burn API credits
- The ONLY cost is the X/Twitter rewrite (~$0.04 per publish via Opus)
