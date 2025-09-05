import os, pickle, json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None
    # Use GitHub secret path in Actions
    if os.path.exists("token.pkl"):
        creds = pickle.load(open("token.pkl", "rb"))
    else:
        credentials_json = os.environ.get("GCP_CREDENTIALS")
        if not credentials_json:
            raise ValueError("GCP_CREDENTIALS environment variable not set")
        
        creds_data = json.loads(credentials_json)
        with open("temp_credentials.json", "w") as f:
            json.dump(creds_data, f)

        flow = InstalledAppFlow.from_client_secrets_file("temp_credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.pkl", "wb") as f:
            pickle.dump(creds, f)
        
        os.remove("temp_credentials.json")  # clean up

    return build("calendar", "v3", credentials=creds)
