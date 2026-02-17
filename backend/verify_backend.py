
import requests
import json

def test_best_time():
    url = "http://127.0.0.1:8000/best_time?day=12&hour=8&station=Dadar&rain=10&delay=5&temp=30&weekend=0"
    try:
        response = requests.get(url)
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_best_time()
