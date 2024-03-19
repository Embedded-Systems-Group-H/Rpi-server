import requests
import time
import json

from config import *

def start_session(session_id):
    try:
        url = f"http://{SERVER_IP}:{SERVER_PORT}/api/session_start/{session_id}"
        response = requests.post(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to send data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def end_session(session_id):
    try:
        url = f"http://{SERVER_IP}:{SERVER_PORT}/api/session_end/{session_id}"
        response = requests.post(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to send data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def send_gps(session_id, ts, lat, long):
    # /api/gps/<id>?ts=<ts>&lat=<lat>&long=<long>
    try:
        params = {"ts": str(ts), "lat": str(lat), "long": str(long)}
        # url = f"http://{SERVER_IP}:{SERVER_PORT}/api/gps/{session_id}?ts={ts}&lat={lat}&long={long}"
        url = f"http://{SERVER_IP}:{SERVER_PORT}/api/gps/{session_id}"
        response = requests.post(url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to send data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def send_step_count(session_id, ts, step_count):
    try:
        params = {"ts": str(ts), "count": str(step_count)}
        url = f"http://{SERVER_IP}:{SERVER_PORT}/api/step_count/{session_id}"
        response = requests.post(url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to send data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ts = time.time()
    session_id = str(int(ts))

    response = start_session(session_id)
    print(response)

    time.sleep(0.5)

    toggle = False
    for i in range(10):
        ts = time.time()
        lat = 10
        long = 20
        step_count = 1234
        toggle = not toggle

        response = send_step_count(session_id, ts, step_count)
        print(response)
        if toggle:
            response = send_gps(session_id, ts, lat, long)
            print(response)
        
        time.sleep(0.25)

    response = end_session(session_id)
    print(response)