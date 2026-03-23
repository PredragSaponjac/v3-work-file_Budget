# ORCA V3 Budget — Manual Workflow (Zero API Cost)

## Why Manual?
The automated pipeline (`pipeline_v20.py`) calls Claude, GPT, and Gemini APIs
which costs money. In manual mode, YOU are the API — paste the same prompts
into AI desktop apps for free. Same quality, zero cost.

---

## DAYTIME: Catalyst Hunt (Mon-Fri 9:30 AM / 1:00 PM / 3:00 PM CT)

You will receive a Telegram reminder at each time with exact instructions.

### Step 1: Catalyst Hunt (3 models independently)

Open `prompts/r1_master_v5_3.txt` — this is your R1 prompt.

Paste it into ALL THREE AI desktops:
1. **Claude desktop** → paste prompt → send → save output as `claude_ideas.txt`
2. **ChatGPT** → paste prompt → send → save output as `gpt_ideas.txt`
3. **Gemini** → paste prompt → send → save output as `gemini_ideas.txt`

Each AI hunts catalyst ideas independently using its own knowledge + browsing.
No input data needed — the prompt is self-contained.

Save all 3 files to: `C:\Users\18329\Downloads\v3-work-file_Budget\orca_results\`

### Step 2: Consensus

Bring the 3 outputs back to Claude Code:
```
python consensus.py claude_ideas.txt gpt_ideas.txt gemini_ideas.txt
```

This merges the best ideas from all 3 models.

### Step 3: Publish

```
python publish.py consensus_output.txt
```

Sends to Telegram + X.

---

## OVERNIGHT: Teacher / Reviewer (Mon-Fri 8:00 PM CT)

The overnight pipeline has 3 layers:

| Layer | What it does | Cost | Manual? |
|---|---|---|---|
| Layer 1 | Thesis tracking, PnL snapshots, horizon outcomes | FREE | Runs automatically |
| Layer 2 | Replay analysis (cheap models) | $$ | YES — paste into AI desktop |
| Layer 3 | Premium deep review (Opus) | $$$ | YES — paste into AI desktop |

### Layer 1 (automatic, free)
Runs via GitHub Actions or locally. No manual work needed.
Tracks open theses, marks PnL, records overnight price moves.

### Layer 2 + 3 (manual)
If there are open theses that need review:
1. Open thesis files from `orca_v20/` or database
2. Paste review prompts into Claude/GPT desktop
3. Save outputs back for the pipeline to learn from

**Note**: If no active theses, overnight has nothing to review — skip.

---

## AUTOMATED REMINDERS (GitHub Actions)

| Time | What | Workflow |
|---|---|---|
| 9:30 AM CT | Telegram: "Run ORCA catalyst hunt" | `orca_manual_reminder.yml` |
| 1:00 PM CT | Telegram: "Run ORCA midday update" | `orca_manual_reminder.yml` |
| 3:00 PM CT | Telegram: "Run ORCA afternoon scan" | `orca_manual_reminder.yml` |

These are Telegram-only reminders — zero API cost, just a ping telling you what to do.

---

## Key Files
| File | Purpose |
|---|---|
| `prompts/r1_master_v5_3.txt` | R1 catalyst hunter prompt (paste into AI desktops) |
| `prompts/catalyst_confirmation_v2.txt` | Confirmation prompt (optional Stage 2) |
| `prompts/flow_module_v5_7.txt` | UW flow analysis prompt |
| `prompts/methodology_note.txt` | Methodology context |
| `send_reminder.py` | Telegram reminder script |
| `MANUAL_WORKFLOW.md` | This file |

---

## What NOT to do
- Do NOT run `pipeline_v20.py` — it calls paid APIs (Claude/GPT/Gemini)
- Do NOT run `overnight_v20.py` with Layer 2/3 — it calls paid APIs
- Do NOT enable old scheduled tasks in Claude Code — they burn API credits
- Do NOT enable old GitHub workflows (`orca_v20_budget_sprint.yml`, `orca_v20_budget_overnight.yml`)
- The ONLY paid API call is the X/Twitter rewrite (~$0.04 per publish via Opus)
