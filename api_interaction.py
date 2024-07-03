import requests
import json

def send_message(message, recipients):
    url = 'http://IP:8080/v2/send'
    data = {
        "message": message,
        "number": "PHONENUMBER",  # Adjust as needed
        "recipients": recipients
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def receive_messages():
    url = 'http://IP:8080/v1/receive/%2BPHONE?ignore_attachments=true&ignore_stories=true'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()
