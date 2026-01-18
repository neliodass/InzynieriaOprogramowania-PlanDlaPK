import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_mock_data():
    print("Testing /schedule with mock data...")
    data = {
        "use_mock_data": True,
        "num_classes": 10,
        "num_rooms": 3,
        "num_slots": 15,
        "target_score": 300,
        "max_attempts": 5
    }
    response = requests.post(f"{BASE_URL}/schedule", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Success: {result.get('success')}")
    print(f"Score: {result.get('score')}")
    print(f"Schedule entries: {len(result.get('schedule', []))}\n")

def test_custom_data():
    print("Testing /schedule with custom data...")
    with open('example_custom_request.json', 'r') as f:
        data = json.load(f)
    response = requests.post(f"{BASE_URL}/schedule", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Success: {result.get('success')}")
    print(f"Score: {result.get('score')}")
    print(f"Schedule entries: {len(result.get('schedule', []))}\n")

if __name__ == "__main__":
    print("=" * 50)
    print("API Testing")
    print("=" * 50 + "\n")

    try:
        test_health()
        test_mock_data()
        test_custom_data()
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the server is running (python api.py)")
    except Exception as e:
        print(f"Error: {e}")

