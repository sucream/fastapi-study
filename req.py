import requests

res = requests.post("http://localhost:8000/todos", json={
  "contents": "할 일 내용",
  "is_done": False
})

print(res.json())