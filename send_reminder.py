#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ORCA Budget — Telegram Reminder
================================

Sends a Telegram message telling the user exactly what to do.
Called by GitHub Actions on schedule.

Usage:
    python send_reminder.py --session morning
    python send_reminder.py --session midday
    python send_reminder.py --session afternoon
"""

import os
import sys
import argparse
import requests
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass


SESSIONS = {
    "morning": {
        "time": "9:30 AM CT",
        "emoji": "\U0001f305",
        "note": "Market just opened. Fresh catalyst hunt.",
    },
    "midday": {
        "time": "1:00 PM CT",
        "emoji": "\u2600\ufe0f",
        "note": "Midday update. Check for new developments since morning.",
    },
    "afternoon": {
        "time": "3:00 PM CT",
        "emoji": "\U0001f307",
        "note": "Final scan before close. Last chance for today's setups.",
    },
}


def send_telegram(token, chat_id, message):
    """Send message via Telegram Bot API (sync, no library needed)."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code == 200:
        print(f"[TG] Reminder sent ({len(message)} chars)")
    else:
        print(f"[TG] ERROR {resp.status_code}: {resp.text}")
    return resp.status_code == 200


def build_reminder(session_key):
    session = SESSIONS[session_key]
    date_str = datetime.now().strftime("%Y-%m-%d")
    day_name = datetime.now().strftime("%A")

    msg = (
        f"{session['emoji']} <b>ORCA CATALYST HUNT — {day_name} {session['time']}</b>\n"
        f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
        f"<i>{session['note']}</i>\n\n"
        f"<b>STEP 1: Paste prompt into 3 AI desktops</b>\n"
        f"Open: <code>prompts/r1_master_v5_3_manual.txt</code>\n\n"
        f"Paste into:\n"
        f"  1\ufe0f\u20e3 Claude desktop \u2192 save as <code>claude_ideas.txt</code>\n"
        f"  2\ufe0f\u20e3 ChatGPT \u2192 save as <code>gpt_ideas.txt</code>\n"
        f"  3\ufe0f\u20e3 Gemini \u2192 save as <code>gemini_ideas.txt</code>\n\n"
        f"<b>STEP 2: Bring outputs to Claude Code</b>\n"
        f"Run consensus on all 3 outputs.\n\n"
        f"<b>STEP 3: Publish</b>\n"
        f"<code>python publish.py consensus_output.txt</code>\n\n"
        f"\u26a0\ufe0f Do NOT run pipeline_v20.py \u2014 it burns API credits!\n"
        f"\U0001f4c5 {date_str}"
    )
    return msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True, choices=["morning", "midday", "afternoon"])
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()

    msg = build_reminder(args.session)

    if args.dry_run:
        import re
        print(re.sub(r'<[^>]+>', '', msg))
        return

    token = os.environ.get("SPY_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or os.environ.get("SPY_CHANNEL_ID")

    if not token or not chat_id:
        print("[ERROR] SPY_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        sys.exit(1)

    send_telegram(token, chat_id, msg)


if __name__ == "__main__":
    main()
