import requests

# Define the Rasa Action Server host and endpoint
# rasa_host = "http://0.0.0.0:5005/webhook"

# Define the message/query you want to send to the server
query_text = "  anh giáp chưa có người yêu, nên làm gì"
# NLP
conver_text = query_text.lower()
# remove special, ?..
# Send a POST request to the Rasa Action Server
response = requests.post('http://127.0.0.1:5005/webhooks/rest/webhook', json={"sender": "test", "message": query_text})
# Check the response from the server
if response.status_code == 200:
    print("Response from Rasa Action Server:", response.json())
else:
    print(f"Failed to get a response. Status code: {response.status_code}")