import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("1. Testing GET /tasks/")
response = requests.get(f"{BASE_URL}/tasks/")
print(f"Status: {response.status_code}")
print(f"Tasks: {response.json()}")
print()

print("2. Creating a new task...")
new_task = {
    "title": "Learn DRF Today",
    "description": "Build REST API",
    "status": "in_progress"
}
response = requests.post(f"{BASE_URL}/tasks/", json=new_task)
print(f"Status: {response.status_code}")
task_data = response.json()
print(f"Created Task: {task_data}")
task_id = task_data.get('id')
print()

print("3. Testing GET /tasks/{task_id}/")
response = requests.get(f"{BASE_URL}/tasks/{task_id}/")
print(f"Status: {response.status_code}")
print(f"Task Details: {response.json()}")
print()

print("4. Testing complete action")
response = requests.post(f"{BASE_URL}/tasks/{task_id}/complete/")
print(f"Status: {response.status_code}")
print(f"Complete Response: {response.json()}")
print()

print("5. Testing filtered GET")
response = requests.get(f"{BASE_URL}/tasks/?status=completed")
print(f"Status: {response.status_code}")
print(f"Completed Tasks: {response.json()}")