import requests

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz-560m"

response = requests.post(
    API_URL,
    headers={},  
    json={"inputs": "Summarize climate change in 3 bullet points."},
    timeout=30
)

print("Status Code:", response.status_code)

if response.status_code == 200:
    print(" Response:")
    print(response.json())
else:
    print(" Error:")
    print(response.text)
