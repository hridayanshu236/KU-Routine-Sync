import os
import requests

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send_discord_alert(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("❌ Discord webhook not set")
        return
    
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    
    if response.status_code == 204:
        print("✅ Discord alert sent successfully!")
    else:
        print(f"❌ Failed to send alert. Status code: {response.status_code}")
