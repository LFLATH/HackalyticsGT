import datetime
import requests
import pandas as pd

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY_DATAS = ["dewpoint_2m", "precipitation","pressure_msl","cloudcover","windspeed_10m","winddirection_10m", "temperature_2m"]
METERS = ["electricity", "chilledwater", "steam", "hotwater"]
FIELDS = ["primary_use_ordinal", "square_feet", "year_built", "floor_count", "air_temperature", "cloud_coverage", "dew_temperature",
"precip_depth_1_hr", "sea_level_pressure", "wind_direction", "wind_speed", "day_of_week", "month", "day", "hour"]

CONVERSION_DICT = {
    "time": "timestamp",
    "temperature_2m": "air_temperature",
    "cloudcover": "cloud_coverage",
    "dewpoint_2m": "dew_temperature",
    "precipitation": "precip_depth_1_hr",
    "pressure_msl": "sea_level_pressure",
    "windspeed_10m": "wind_speed",
    "winddirection_10m": "wind_direction",
}

AUTH_URL = "https://api.precisely.com/oauth/token"
ADDRESS_URL = "https://api.precisely.com/property/v2/attributes/byaddress"
BASE64_KEY = "Basic NTJjdEtaczdudFJZQ1o1b2JPbWpuZ2dHdjNSMFB5T1Y6Szh3U0gzcHhBeXhzdDZxMw=="

def get_historical_weather(lat, long, days=1):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    params = dict(
        latitude=lat,
        longitude=long,
        hourly=",".join(HOURLY_DATAS),
        windspeed_unit="ms",
        timeformat="unixtime",
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
    )
    param_str = "&".join(f"{k}={v}" for k, v in params.items())
    res = requests.get(f"{WEATHER_URL}?{param_str}")
    res.raise_for_status()
    res_json = res.json()
    df = pd.DataFrame(res_json["hourly"])
    df.rename(columns=CONVERSION_DICT, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit="s")
    df['cloud_coverage'] = df['cloud_coverage'] / 100 * 8  # percentage to oktal (?)
    return df

def get_precisely_auth():
    r = requests.post(AUTH_URL, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": BASE64_KEY,
    }, data="grant_type=client_credentials",
    )
    r.raise_for_status()
    res_json = r.json()
    return res_json["access_token"]


def precisely_get_address_details(address, auth):
    auth_str = f"Bearer {auth}"
    r = requests.get(ADDRESS_URL, params={
        "address": address,
        "attributes": "all",
    }, headers={"Authorization": auth_str}
    )
    r.raise_for_status()
    res_json = r.json()
    if "propertyAttributes" not in res_json:
        print("no geo data found")
        return {
        "square_feet": 5000,
        "year_built": 2000,
        "primary_use": "Lodging/residential",
        "floor_count": 4
    }
    
    attrs = res_json["propertyAttributes"]
    sqft = int(attrs.get("buildgSqFt"))
    year = int(attrs.get("builtYear")) or int(attrs.get("effectiveBuiltYear"))
    proptype = attrs.get("propType")
    floor_count = 4
    stories = attrs.get("stories")
    if stories:
        floor_count = stories.get("value")
        try:
            floor_count = int(floor_count)
        except:
            floor_count = 4
    d = {
        "R": "Lodging/residential",
        "C": "Office",
        "V": "Other",
        "X": "Other",
        None: "Lodging/residential"
    }
    primary_usage = d.get(proptype, "Other")
    return {
        "square_feet": sqft,
        "year_built": year,
        "primary_use": primary_usage,
        "floor_count": floor_count
    }
