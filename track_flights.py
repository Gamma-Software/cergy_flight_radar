from opensky_api import OpenSkyApi, StateVector
import csv
from os import path
import pandas as pd
import sys


def credentials(filename):
    # Get credentials
    f = open(filename, "r")
    return f.read().splitlines()


def get_flights_from_loc(usr, pwd, loc):
    # Get flights in the specific location
    api = OpenSkyApi(usr, pwd)
    return api.get_states(bbox=loc)


def save_flights(filename, with_header=False):
    columns = StateVector.keys
    columns.insert(0, 'timestamp')
    if with_header:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
        csvfile.close()
    with open(filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        # iterate over flights in the current time flying above Cergy
        dict_to_save = {'timestamp': states.time}
        if states.states:
            for flight in states.states:
                dict_to_save.update(flight.__dict__)
                writer.writerow(dict_to_save)
    csvfile.close()


def get_number_of_flight_in_day(filename):
    df = pd.read_csv(filename)
    del df["sensors"]
    del df["squawk"]
    del df["icao24"]
    del df["time_position"]
    del df["last_contact"]
    del df["longitude"]
    del df["latitude"]
    del df["on_ground"]
    del df["spi"]
    del df["position_source"]
    df = df.drop_duplicates(subset=['callsign'])
    # Remove airplane passing over Cergy higher than 5000 feet
    df = df.drop(df[df.geo_altitude > 5000].index)
    df.timestamp = pd.to_datetime(df.timestamp, unit='s').dt.normalize()
    df["day"] = df.timestamp.dt.day
    df["month"] = df.timestamp.dt.month
    df["year"] = df.timestamp.dt.year
    df2 = df[["day"]].assign(numberplane=0)
    df3 = df2.groupby(by=["day"]).count()
    return int(df3.iloc[-1]["numberplane"])


credential = credentials(sys.argv[1])

# Cergy GPS Bounding Box
cergy_location = (49.040316, 49.049739, 2.006292, 2.029595)
states = get_flights_from_loc(credential[0], credential[1], cergy_location)

# Save those flights
try:
    save_flights(sys.argv[3], not path.exists(sys.argv[3]))
except IOError:
    print("I/O error")

# Send the number of plane to mqtt
import paho.mqtt.publish as publish
f = open(sys.argv[2], "r")
mqtt_credential = f.read().splitlines()
print(mqtt_credential[0], mqtt_credential[1])
number_of_plane = get_number_of_flight_in_day(sys.argv[3])
publish.single("home/raspi/cergy_flights", payload=number_of_plane, hostname='192.168.1.38',
               auth={'username': mqtt_credential[0], 'password': mqtt_credential[1]})
print("Message ", number_of_plane, " is delivered in the topic home/raspi/cergy_flights")
