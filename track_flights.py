from opensky_api import OpenSkyApi, StateVector

# Get credentials
f = open("credential.txt", "r")
credential = f.read().splitlines()

# Cergy GPS Bounding Box
cergy_location = (49.013780, 49.057670, 1.991615, 2.086029)

# Get flights in the specific location
api = OpenSkyApi(credential[0], credential[1])
states = api.get_states(bbox=cergy_location)
print(states)