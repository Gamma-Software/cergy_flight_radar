from opensky_api import OpenSkyApi, StateVector
import csv
from os import path
import pandas as pd


def credentials(filename):
    # Get credentials
    f = open(filename, "r")
    return f.read().splitlines()


def get_flights_from_loc(usr, pwd, loc):
    # Get flights in the specific location
    api = OpenSkyApi(usr, pwd)
    return api.get_states(bbox=loc)


def save_flights(with_header=False):
    columns = StateVector.keys
    columns.insert(0, 'timestamp')

    # Get the last flights saved
    df = pd.read_csv("flights_over_cergy.csv")["timestamp", "callsign"]

    # Get the last minute flights
    # https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/09_timeseries.html
    df.timestamp.dt.day.hour.minute

    if with_header:
        with open("flights_over_cergy.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
    with open("flights_over_cergy.csv", 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        # iterate over flights in the current time flying above Cergy
        dict_to_save = {'timestamp': states.time}
        if states.states:
            for flight in states.states:
                dict_to_save.update(flight.__dict__)
                writer.writerow(dict_to_save)


credential = credentials("credential.txt")

# Cergy GPS Bounding Box
cergy_location = (49.013780, 49.057670, 1.991615, 2.086029)
states = get_flights_from_loc(credential[0], credential[1], cergy_location)

# Save those flights
try:
    save_flights(not path.exists("flights_over_cergy.csv"))
except IOError:
    print("I/O error")




