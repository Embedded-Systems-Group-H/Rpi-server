# this script will handle the incoming csv file, and convert them into the correct form to display on the webpage 
from datetime import datetime
import csv
import pandas as pd
import time
import mpu

def csv_handle(filename):
    rows = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    data = pd.read_csv(filename)
    return rows

def get_datetime(UnixDateTime):
    current_date_time = datetime.fromtimestamp(UnixDateTime)
    # print("date_time", current_date_time)
    return current_date_time

def get_distance(data): # this function return the total distance of a workout 
    distance = 0
    data_length = len(data)
    print (data_length)
    for i in range (data_length-1):
        # print(i)
        lat1 = data.latitude[i]
        lon1 = data.longitude[i]
        lat2 = data.latitude[i+1]
        lon2 = data.longitude[i+1]
        dist = mpu.haversine_distance((lat1,lon1), (lat2, lon2))
        distance = distance + dist
    return round(distance,2)

def get_step(data):
    data_length = len(data)
    # print(data.stepcount)
    return data.stepcount[data_length-1]

def get_calories(duration):
    body_weight = 75
    MET = 6 #this is the recommended MET for jogging
    calories = duration * MET * 3.5 * body_weight / (200*60)
    return int(calories)

def get_coordinates(data):
    coordinates = []
    for i in range(len(data)):
        coordinates.append([data.longitude[i], data.latitude[i]])
    return coordinates

def construct_csv_string(data):
    csv_string= "\n"
    # data = pd.read_csv(filename)
    current_datetime = get_datetime(data.timestamp[0])
    csv_string = csv_string + str(current_datetime)+","  # add the date time to the csv
    data_length = len(data.timestamp) # number of row in the csv file
    duration = data.timestamp[data_length-1]- data.timestamp[0] # last row timestamp - first row timestamp
    minute_second = time.strftime("%H:%M:%S", time.gmtime(duration))
    csv_string = csv_string + minute_second + "," # add minute second to string
    distance = get_distance(data)
    csv_string = csv_string + str(distance) + "," # add distance to string 
    steps = get_step(data)
    csv_string = csv_string + str(steps) + "," # add step to string
    calories = get_calories(duration)
    csv_string = csv_string + str(calories) #add calories to string
    coordinates = get_coordinates(data)
    csv_string += ',' + str(coordinates)
    return csv_string

if __name__ == "__main__":
    csv_filename = "testfile2.csv"
    write_filename = "summary.csv"
    data = pd.read_csv(csv_filename)
    print('data', data)
    string_to_append = construct_csv_string(data)
    f = open(write_filename, "a")
    f.write(string_to_append)
    f.close()