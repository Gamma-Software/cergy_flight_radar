from opensky_api import OpenSkyApi, StateVector

import csv
import os.path
from os import path

# Get credentials
f = open("credential.txt", "r")
credential = f.read().splitlines()

# Cergy GPS Bounding Box
cergy_location = (49.013780, 49.057670, 1.991615, 2.086029)

# Get flights in the specific location
api = OpenSkyApi(credential[0], credential[1])
states = api.get_states(bbox=cergy_location)
#states = api.get_states()

columns = StateVector.keys
columns.insert(0, 'timestamp')

# Save those flights
try:
    if not path.exists("flights_over_cergy.csv"):
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
            else:
                writer.writerow(dict_to_save)
    else:
        with open("flights_over_cergy.csv", 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            # iterate over flights in the current time flying above Cergy
            dict_to_save = {'timestamp': states.time}
            if states.states:
                for flight in states.states:
                    dict_to_save.update(flight.__dict__)
                    writer.writerow(dict_to_save)
            else:
                writer.writerow(dict_to_save)

except IOError:
    print("I/O error")




