
import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1413368775566299136/PSrcRfpNNRjPEpvwL7gzpCJ0ROb8GzIMItiTDc3kEHX45FOZDrJDi1JfopmiCqgp91hW"

def send_discord_alert(message: str):
    """Send a message to Discord channel via webhook"""
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    
    if response.status_code == 204:
        print("✅ Discord alert sent successfully!")
    else:
        print(f"❌ Failed to send alert. Status code: {response.status_code}")

