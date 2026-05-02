<<<<<<< HEAD
import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "Feature1": 100,
    "Feature2": 200,
    "Feature3": 300,
    "Feature4": 400
}

response = requests.post(url, json=data)

=======
import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "Feature1": 100,
    "Feature2": 200,
    "Feature3": 300,
    "Feature4": 400
}

response = requests.post(url, json=data)

>>>>>>> 62378f46b605f4d73ef0fa7d1153e9aff172100e
print(response.json())