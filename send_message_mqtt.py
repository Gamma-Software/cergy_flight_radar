import sys
import paho.mqtt.publish as publish

f = open("credential_mqtt.txt", "r")
credential = f.read().splitlines()


def get_number_of_flight_in_day(filename):
    import pandas as pd
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


if __name__ == "__main__":
    print(sys.argv[1])
    number_of_plane = get_number_of_flight_in_day(sys.argv[1])
    publish.single("home/raspi/cergy_flights", payload=number_of_plane, hostname='192.168.1.38',
                   auth={'username': credential[0], 'password': credential[1]})
    print("Message ", number_of_plane, " is delivered in the topic home/raspi/cergy_flights")