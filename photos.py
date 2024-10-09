from flask import Flask, redirect, request, session, url_for, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

# Remove API_KEY as it's not used and shouldn't be exposed
# API_KEY= "AIzaSyAhPGd0-Q6GIuYvAYDaB23y7ImTFUpxvac"

# Replace these with your client ID and client secret
client_id = '708091353653-banei10l291n3hqc5e55a060ua205ru4.apps.googleusercontent.com'
client_secret = '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'

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Consider using a more secure secret key
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Only for development, remove in production

# Define the OAuth 2.0 flow without client_secret.json
flow = Flow.from_client_config(
    {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:5000/callback"],
            "scopes": ["https://www.googleapis.com/auth/photoslibrary.readonly"]
        }
    },
    scopes=["https://www.googleapis.com/auth/photoslibrary.readonly"]
)

@app.route('/')
def index():
    # Check if the credentials exist in the session
    if 'credentials' not in session:
        return redirect('/authorize')

    try:
        # Use the stored credentials
        credentials = Credentials(
            session['credentials']['token'],
            refresh_token=session['credentials'].get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret
        )
        service = build('photoslibrary', 'v1', credentials=credentials)

        # Fetch the list of media items from the specified album
        album_id = "YOUR_ALBUM_ID"  # Replace with your actual album ID
        results = service.mediaItems().search(body={"albumId": album_id, "pageSize": 5}).execute()
        items = results.get('mediaItems', [])

        # Return the latest 5 photo URLs
        return jsonify({
            "photos": [item['baseUrl'] for item in items]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/authorize')
def authorize():
    # Start the OAuth authorization flow
    authorization_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    try:
        # Fetch token after the user consents
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials

        # Save the credentials in session for future use
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token
        }

        return redirect('/')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
