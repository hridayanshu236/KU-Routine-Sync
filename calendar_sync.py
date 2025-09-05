import datetime
import pytz

days = {
    "Sunday": 6,
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
}

TIMEZONE = "Asia/Kathmandu"
tz = pytz.timezone(TIMEZONE)

SEMESTER_START = datetime.date(2025, 9, 7)  # first Sunday
WEEKS = 20  # number of weeks

# Subject code → full subject name
SUBJECT_NAMES = {
    "COMP 343": "Information System Ethics",
    "COMP 306": "Embedded Systems",
    "COMP 304": "Operations Research",
    "COMP 342": "Computer Graphics",
    "COMP 314": "Algorithms and Complexity",
    "COMP 302": "System Analysis and Design",
    "COMP 308": "Combined Engineering Project",
}

# Codes that should be skipped (holidays / project days)
HOLIDAYS = ["COMP 308"]

def add_event(service, day, time_range, subject_code, teacher, room):
    """Create one recurring Google Calendar event with:
       - title = subject code
       - description = subject name - teacher
       - participant = mkju84sumi@gmail.com (no email sent)
    """
    # Skip holidays
    if subject_code in HOLIDAYS:
        print(f"Skipping {subject_code} on {day} ({time_range}) – holiday / project day")
        return

    start_time, end_time = time_range.split("-")
    sh, sm = map(int, start_time.split(":"))
    eh, em = map(int, end_time.split(":"))

    weekday = days.get(day)
    if weekday is None:
        return

    today = datetime.datetime.now(tz).date()  # today in Kathmandu timezone
    delta = (weekday - today.weekday()) % 7
    event_date = today + datetime.timedelta(days=delta)

    start_dt = tz.localize(datetime.datetime(event_date.year, event_date.month, event_date.day, sh, sm))
    end_dt = tz.localize(datetime.datetime(event_date.year, event_date.month, event_date.day, eh, em))

    subject_name = SUBJECT_NAMES.get(subject_code, "Unknown Subject")

    event = {
    "summary": subject_code,  # Title = code
    "location": room if room else "",
    "description": f"{subject_name} - {teacher}" if teacher else subject_name,
    "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
    "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
    "recurrence": [f"RRULE:FREQ=WEEKLY;COUNT={WEEKS}"],
    "attendees": [{"email": "mkju84sumi@gmail.com"}]
}


    # Insert event without sending emails
    service.events().insert(
        calendarId="primary",
        body=event,
        sendUpdates="none"  # no email sent
    ).execute()

    print(f" Added {subject_code}: {subject_name} ({teacher}) on {day} {time_range} at {room}")

def clear_future_semester_events(service):
    """Delete all future events in the semester period starting from today"""
    from datetime import datetime, timedelta

    tzinfo = pytz.timezone(TIMEZONE)
    today = datetime.now(tzinfo).date()  # fixed: use datetime.now, not datetime.datetime.now
    start = tzinfo.localize(datetime(today.year, today.month, today.day))
    end = start + timedelta(weeks=WEEKS)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True
    ).execute()

    events = events_result.get("items", [])
    for e in events:
        service.events().delete(calendarId="primary", eventId=e["id"]).execute()
        print(f"Deleted future event: {e['summary']}")



