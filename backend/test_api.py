import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "Feature1": 100,
    "Feature2": 200,
    "Feature3": 300,
    "Feature4": 400
}

response = requests.post(url, json=data)

print(response.json())