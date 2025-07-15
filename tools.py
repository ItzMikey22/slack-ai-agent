from datetime import datetime
import json
import os

def load_shifts():
    with open('shifts.json') as f:
        return json.load(f)

def load_blocked():
    with open('blocked.json') as f:
        return json.load(f)

def is_blocked(date_str):
    blocked = load_blocked()
    return date_str in blocked

def is_free(start_time, end_time):
    shifts = load_shifts()
    for shift in shifts:
        shift_start = datetime.strptime(shift["start"], "%Y-%m-%d %H:%M")
        shift_end = datetime.strptime(shift["end"], "%Y-%m-%d %H:%M")
        if start_time < shift_end and end_time > shift_start:
            return False
    return True
