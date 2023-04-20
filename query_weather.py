import requests
import datetime
import yaml

def get_weather(p_lat, p_lon, p_datetime):

    with open("configs.yaml", "r") as f:
        config = yaml.safe_load(f)     
        weather_api_key = config['weather']['APIkey']
        # p_lat = latitude value of the earthquake
        # p_lon = longitude value of the earthquake   
        # p_datetime = datetime object with date & time of earthquake
        # my_api_key = the API key obtained with my free account

        method="GET"
        url_base="https://api.weatherapi.com/v1/history.json"
        pars = {
               "q": f"{p_lat},{p_lon}",
               "dt": str(p_datetime.date()),
               "key": weather_api_key,
         }
    response_json = requests.request(
           method=method,
           url=url_base,
           params=pars
).json()
    # p_datetime = datetime object with date & time of earthquake
    # First obtain all 1-hour blocks before the specified time.
    # This assumes the weather_response contains weather on the
    # day of the earthquake.
    weather_hour_early_list = \
          [hr for hr in
           response_json["forecast"]["forecastday"][0]["hour"]
           if hr["time_epoch"] < p_datetime.timestamp()]
    # Now choose the last hour block before the earthquake’s time.
    weather_hour = weather_hour_early_list[-1]
    temp_f = weather_hour["temp_f"]
    return temp_f

