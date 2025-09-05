from detect_changes import routine_changed
from parse_routine import parse_routine
from auth_calendar import get_calendar_service
from calendar_sync import add_event, clear_future_semester_events
from discord_alerts import send_discord_alert  

if __name__ == "__main__":
    changed, html = routine_changed()
    if changed:
        print("Routine updated! Syncing to Google Calendar...")
        routine = parse_routine(html)
        service = get_calendar_service()

        # Clear only future events from today to avoid duplicates
        clear_future_semester_events(service)

        # Add updated events starting from today / next occurrence
        for entry in routine:
            add_event(service, *entry)

        print("✅ Calendar synced successfully!")

        # Send Discord alert
        send_discord_alert("🚨 @everyone KU Routine has been updated! Google Calendar synced successfully.")

    else:
        print("No change detected. Calendar is up-to-date.")
