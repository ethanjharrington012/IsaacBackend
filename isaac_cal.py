from __future__ import print_function
import datetime
import json
import os.path
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import webbrowser
from google.auth.exceptions import RefreshError
import traceback
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_events():
    """Shows basic usage of the Google Calendar API.
    Returns the start and name of the next 10 events on the user's calendar.
    """
    creds = None

    # The file token.json stores the user's access and refresh tokens
    # and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If credentials are not available or are invalid, initiate the OAuth flow
    if not creds or not creds.valid:
        # Handle token refresh if credentials have expired
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                os.remove('token.json')
                return get_calendar_events()
        else:
            client_id = os.getenv('GOOGLE_CLIENT_ID')
            client_secret = os.getenv('GOOGLE_CLIENT_SECRET')   
            # If no valid credentials, initiate the flow to get them
            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["http://localhost"]
                }
            }, SCOPES)

            creds = flow.run_local_server(port=0, host='127.0.0.1')
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting events from Show Events calendar')
        
        # First, get the calendar ID for "Show Events"
        calendar_list = service.calendarList().list().execute()
        show_events_calendar = next((calendar for calendar in calendar_list['items'] if calendar['summary'] == 'Show Events'), None)
        
        if not show_events_calendar:
            print('Show Events calendar not found.')
            return []
        
        calendar_id = show_events_calendar['id']
        
        events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        event_data = []

        if not events:
            print('No upcoming events found in Show Events calendar.')
            return event_data

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            location = event.get('location', 'No location')
            attachments = event.get('attachments', [])
            
            print(start, event['summary'], event.get('description', 'No description'), location)

            event_data.append({
                'title': event['summary'],
                'description': event.get('description', 'No description'),
                'start': start,
                'location': location,
                'attachments': [
                    {
                        'fileUrl': attachment.get('fileUrl'),
                        'mimeType': attachment.get('mimeType'),
                        'title': attachment.get('title')
                    } for attachment in attachments
                ]
            })

        return event_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


@app.route('/')
def index():
    return "Welcome to the Calendar Events API. Use /api/events to get events."

@app.route('/api/events', methods=['GET'])
def events():
    """API endpoint to get calendar events."""
    try:
        events = get_calendar_events()
        return jsonify(events)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({"error": error_message}), 500

# Add this error handler
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle exceptions globally"""
    error_message = f"An unexpected error occurred: {str(e)}\n{traceback.format_exc()}"
    print(error_message)
    return jsonify({"error": error_message}), 500

print("Calendar events will be available at: http://127.0.0.1:5000/api/events")

if __name__ == '__main__':
    print("Starting the server. Please authorize the application if prompted.")
    print("After authorization, the calendar events will be available at: http://localhost:5000/api/events")
    webbrowser.open('http://localhost:5000/api/events')
    app.run(port=5000)