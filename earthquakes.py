import requests
import time as true_time
import datetime
from query_weather import get_weather
import pandas as pd


def earthquake(n=3.0):
    n = float(n)
    list_of_earthquakes = []

    method = "GET"
    url_base = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
    hour_ago = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat()
    right_now = (
        datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
    ).isoformat()

    pars = {"format": "geojson", "starttime": f"{hour_ago}", "endtime": f"{right_now}"}
    response_json = requests.request(method=method, url=url_base, params=pars).json()
    features = response_json["features"]

    for i in features:
        title = i["properties"]["title"]
        time_then = i["properties"]["time"]  # Corey told me to ignore timezone for now
        time = datetime.datetime.fromtimestamp(time_then / 1000.00)
        long = i["geometry"]["coordinates"][0]  # odd, but the API does long first
        lat = i["geometry"]["coordinates"][1]
        weather = get_weather(lat, long, time)
        earthquake_dict = {
            "title": title,
            "time": time,
            "lat": lat,
            "long": long,
            "temp_f": weather,
        }

        list_of_earthquakes.append(earthquake_dict)

    df = pd.DataFrame(list_of_earthquakes)
    # need to sort so oldest are lowest index because that's what the example shows
    df = df.sort_values(by="time", ascending=True)
    df.reset_index(drop=True, inplace=True)
    df["temp_f"] = df["temp_f"].fillna(70.0)  # done per Corey's advice
    df["cum_sum_of_last_n"] = df.temp_f.rolling(int(n), min_periods=1).sum()
    df["standard_divisor"] = n
    df["index_plus_one"] = df.index + 1.0
    df["used_divisor"] = df[["standard_divisor", "index_plus_one"]].min(axis=1)
    df["sliding_average_of_last_n"] = df["cum_sum_of_last_n"] / df["used_divisor"]
    print(df[["title", "time", "temp_f", "sliding_average_of_last_n"]])
    # print(df.index.max())

    max_index = df.index.max()
    true_time.sleep(10)  # want "right now" to be distinct from above

    while True:
        # go thru every 15 seconds and scan from 15 seconds ago if there are any quakes

        right_now = (
            datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
        ).isoformat()

        pars = {
            "format": "geojson",
            "starttime": f"{right_now}",
            "endtime": "3033-12-31",
        }
        response_json = requests.request(
            method=method, url=url_base, params=pars
        ).json()

        features = response_json["features"]

        for i in features:
            title = i["properties"]["title"]
            time_then = i["properties"][
                "time"
            ]  # Corey told me to ignore timezone for now
            time = datetime.datetime.fromtimestamp(time_then / 1000.00)
            long = i["geometry"]["coordinates"][0]  # odd, but the API does long first
            lat = i["geometry"]["coordinates"][1]
            weather = get_weather(lat, long, time)
            earthquake_dict = {
                "title": title,
                "time": time,
                "lat": lat,
                "long": long,
                "temp_f": weather,
            }
            list_of_earthquakes.append(earthquake_dict)
            # now, recreate pandas dataframe but only print the new rows
            # we need the last n values to get the sliding average for the
            # new records, so as we appedn to the list it's easier to recreate
            # the entire dataframe from begininning or at least past n values
            df = pd.DataFrame(list_of_earthquakes)
            df = df.drop_duplicates(
                subset=["title", "time"]
            )  # need to drop dupes if always going
            # 15 minutes back while doing it every 15 seconds
            # this way we can test that this loop works while not printing stuff 2x
            # need to sort so oldest are lowest index because that's what the example shows
            df = df.sort_values(by="time", ascending=True)
            df.reset_index(drop=True, inplace=True)
            df["temp_f"] = df["temp_f"].fillna(70.0)  # done per Corey's advice
            df["cum_sum_of_last_n"] = df.temp_f.rolling(int(n), min_periods=1).sum()
            df["standard_divisor"] = n
            df["index_plus_one"] = df.index + 1.0
            df["used_divisor"] = df[["standard_divisor", "index_plus_one"]].min(axis=1)
            df["sliding_average_of_last_n"] = (
                df["cum_sum_of_last_n"] / df["used_divisor"]
            )
            df_new = df[df.index > max_index]
            if df_new.empty:
                pass
            else:
                print(df_new[["title", "time", "temp_f", "sliding_average_of_last_n"]])
            max_index = df.index.max()

        print("waiting\n")

        true_time.sleep(
            15
        )  # sleep for 15 seconds so we're not hitting the API (which is updated every minute


# every 15 seconds and potentially causing them to block us
