import requests

def send_slack_message(text, webhook_url):
    payload = {
        "text": text
    }

    headers = {
        "Content-type": "application/json"
    }

    response = requests.post(webhook_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Message sent successfully to Slack!")
    else:
        print("Failed to send message to Slack. Status code:", response.status_code)


def get_activity():
    response = requests.get("https://www.boredapi.com/api/activity?participants=1&type=recreational")

    if response.status_code == 200:
        item_json = response.json()
        event = item_json["activity"]
        print(f"The activity is: {event}")
        return event



    else: 
        print(f"Bored API failed with status code: {response.status_code}")



# Replace [webhook_url] with your actual webhook URL
webhook_url = "https://hooks.slack.com/services/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"

text_to_send =  get_activity()


send_slack_message(text_to_send, webhook_url)
