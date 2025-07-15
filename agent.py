import openai
import os
from datetime import datetime, timedelta
from tools import is_blocked, is_free
from dotenv import load_dotenv
import re

load_dotenv()
#print("API Key:", os.getenv("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")


def parse_request(msg):
    msg = msg.lower()
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    for day in weekdays:
        if day in msg:
            day_offset = (weekdays.index(day) - datetime.today().weekday()) % 7
            shift_day = datetime.today() + timedelta(days=day_offset)
            time_match = re.search(r'(\d{1,2})(:(\d{2}))?\s*(am|pm)', msg)
            if time_match:
                hour = int(time_match.group(1))
                if time_match.group(4) == "pm" and hour != 12:
                    hour += 12
                start = shift_day.replace(hour=hour, minute=0)
                end = start + timedelta(hours=4)
                return shift_day.strftime("%Y-%m-%d"), start, end
    return None, None, None

def agent_decision(msg):
    day_str, start, end = parse_request(msg)
    if not start or not end:
        return ""  # Don't reply to non-shift messages

    if is_blocked(day_str):
        print(f"🚫 Blocked on {day_str} — staying silent.")
        return ""  # Stay silent — don't reply

    if is_free(start, end):
        return "✅ I'm available to pick that up."
    else:
        print(f"⛔ Already scheduled during this time — staying silent.")
        return ""  # Also stay silent if you're not free

# Test a few cases
if __name__ == "__main__":
    messages = [
        "Can someone take my Friday morning shift?",
        "I need help Sunday at 7am",
        "Anyone want Thursday 1pm to 7pm?",
        "Random message that isn’t about a shift"
        "can someone cover my monday shift 12-5pm"
    ]
    for msg in messages:
        print(f"\n📝 Message: {msg}")
        print(agent_decision(msg))
