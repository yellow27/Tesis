import requests

url = "http://localhost:5000/predict_api"
r = requests.post(url,json={"native":1, "Instructor":1, "Course":1, "Semester":1, "Size":1})
print(r.json())
