from opensky_api import OpenSkyApi, StateVector
import csv
from os import path


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
cergy_location = (49.040316, 49.049739, 2.006292, 2.029595)
states = get_flights_from_loc(credential[0], credential[1], cergy_location)

# Save those flights
try:
    save_flights(not path.exists("flights_over_cergy.csv"))
except IOError:
    print("I/O error")




