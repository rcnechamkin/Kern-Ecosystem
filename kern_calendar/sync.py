from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz
import os
import json

# === Config ===
CREDENTIALS_FILE = "/home/cody/avrana/kern_secrets/credentials.json"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = "cnechamkin@gmail.com"  # ← your actual Gmail, NOT "primary"

def fetch_upcoming_events():
    # Load credentials
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=creds)

    # Date range: now to two weeks from now, in UTC
    local_tz = pytz.timezone("America/Los_Angeles")
    now_local = datetime.now(local_tz)
    future_local = now_local + timedelta(days=14)

    time_min = now_local.astimezone(pytz.utc).isoformat()
    time_max = future_local.astimezone(pytz.utc).isoformat()

    try:
        # Fetch events
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        print(f"📆 Fetched {len(events)} calendar event(s).")

        formatted_events = []
        for event in events:
            start_raw = event['start'].get('dateTime', event['start'].get('date'))
            try:
                dt = datetime.fromisoformat(start_raw.replace('Z', '+00:00'))
                formatted_events.append({
                    'name': event.get('summary', 'Untitled Event'),
                    'date': dt.date().isoformat(),
                    'time': dt.time().strftime('%H:%M') if dt.time() != datetime.min.time() else 'All Day'
                })
            except Exception as e:
                print(f"⚠️ Skipping event due to date parse error: {e}")
                continue

        return formatted_events

    except Exception as e:
        print(f"❌ Failed to fetch calendar events: {e}")
        return []

