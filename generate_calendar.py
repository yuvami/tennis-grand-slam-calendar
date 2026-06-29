#!/usr/bin/env python3
"""Generates ICS calendar with Grand Slam tennis men's finals."""
import uuid
from datetime import date, timedelta

# (year, month, day, hour_utc, title, estimated)
# UTC start times:
#   Australian Open: Melbourne UTC+11 in Jan, final ~7:30PM AEDT = 8:30AM UTC
#   Roland Garros:   Paris UTC+2 in Jun, final ~3:00PM CEST = 1:00PM UTC
#   Wimbledon:       London UTC+1 in Jul, final ~2:00PM BST = 1:00PM UTC
#   US Open:         New York UTC-4 in Sep, final ~4:00PM EDT = 8:00PM UTC
FINALS = [
    # 2026 — confirmed dates
    (2026, 1, 25, 8,  "Australian Open 2026 - Men's Final", False),
    (2026, 6,  7, 13, "Roland Garros 2026 - Men's Final",   False),
    (2026, 7, 12, 13, "Wimbledon 2026 - Men's Final",        False),
    (2026, 9, 13, 20, "US Open 2026 - Men's Final",          False),
    # 2027 — estimated
    (2027, 1, 31, 8,  "Australian Open 2027 - Men's Final (est.)", True),
    (2027, 6,  6, 13, "Roland Garros 2027 - Men's Final (est.)",   True),
    (2027, 7, 11, 13, "Wimbledon 2027 - Men's Final (est.)",        True),
    (2027, 9, 12, 20, "US Open 2027 - Men's Final (est.)",          True),
    # 2028 — estimated
    (2028, 1, 30, 8,  "Australian Open 2028 - Men's Final (est.)", True),
    (2028, 6,  4, 13, "Roland Garros 2028 - Men's Final (est.)",   True),
    (2028, 7,  9, 13, "Wimbledon 2028 - Men's Final (est.)",        True),
    (2028, 9, 10, 20, "US Open 2028 - Men's Final (est.)",          True),
    # 2029 — estimated
    (2029, 1, 27, 8,  "Australian Open 2029 - Men's Final (est.)", True),
    (2029, 6,  8, 13, "Roland Garros 2029 - Men's Final (est.)",   True),
    (2029, 7, 13, 13, "Wimbledon 2029 - Men's Final (est.)",        True),
    (2029, 9,  7, 20, "US Open 2029 - Men's Final (est.)",          True),
]


def fmt_dt(year, month, day, hour):
    return f"{year}{month:02d}{day:02d}T{hour:02d}0000Z"


def generate():
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Grand Slam Tennis Men Finals//EN",
        "X-WR-CALNAME:Grand Slam Men's Finals",
        "X-WR-CALDESC:Men's singles finals for all 4 Grand Slam tournaments",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "REFRESH-INTERVAL;VALUE=DURATION:P1D",
        "X-PUBLISHED-TTL:P1D",
    ]

    for year, month, day, hour, title, estimated in FINALS:
        uid = f"grandslam-{year}{month:02d}{day:02d}-mens-final@yuvami"
        desc_note = "Date is estimated — check official schedule closer to the tournament." if estimated else "Official date."
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART:{fmt_dt(year, month, day, hour)}",
            f"DTEND:{fmt_dt(year, month, day, hour + 3)}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{desc_note}",
            "TRANSP:TRANSPARENT",
            "STATUS:CONFIRMED",
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            "TRIGGER:-P1D",
            f"DESCRIPTION:{title} - tomorrow!",
            "END:VALARM",
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            "TRIGGER:-PT1H",
            f"DESCRIPTION:{title} - starting in 1 hour!",
            "END:VALARM",
            "END:VEVENT",
        ]

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


if __name__ == "__main__":
    content = generate()
    with open("calendar.ics", "w", newline="", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated calendar.ics with {len(FINALS)} events")
