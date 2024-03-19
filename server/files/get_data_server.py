# this is a python script to get send queries to aws server, check if there are any new data, and add the new data to internal csv for display 
# pseudo code: ping the aws server. Send request for all filename available. 
# If filename not found in local 
# then download the file to local folder 
# run data_handle.py to add data to summary.csv 
# the server should automatically update and display the newest set of data 

import requests
import time
import json
import data_handle
from config import *

def get_sessions():
    try:
        url = f"http://{SERVER_IP}:{SERVER_PORT}/api/sessions"
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Failed to send data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def get_session_csv(session_id):
    try:
        url = f"http://{SERVER_IP}:{SERVER_PORT}/api/session_csv/{session_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to send data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        f = open("dataList.txt", "r")
        my_list = f.read().split(",")
        f.close()
        for i in my_list:
            print(i)
        # print(my_list)
        sessions = get_sessions()
        print("Found sessions:")
        print(sessions)
        for session in sessions:
            if session in my_list:
                print ("file " + str(session) + " exist in the list") 
            else: 
                print("cannot find " + str(session) + " in the list")
                print(" prepare to download the file")
                csv = get_session_csv(session)
                # print(csv) 
                #save session to a csv file 
                with open(session, 'w') as file:
                    file.write("timestamp,longitude,latitude,stepcount\n")
                    file.write(csv)
                print("finish writing new file to the server") 
                f = open("dataList.txt", "a")
                f.write(session + ",")
                f.close()
                data_handle.write_to_summary(session)
                # f.write(session)
                # print("added new file name to dataList") 
        print("loop done")
        time.sleep(10)