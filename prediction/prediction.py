import numpy as np
import pandas as pd
import requests
import pickle
import datetime
from matplotlib import pyplot as plt
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import HistGradientBoostingRegressor


URL = "https://api.open-meteo.com/v1/forecast"
hourly = ["dewpoint_2m", "precipitation","pressure_msl","cloudcover","windspeed_10m","winddirection_10m", "temperature_2m"]
meters = ["electricity", "chilledwater", "steam", "hotwater"]
fields = ["primary_use_ordinal", "square_feet", "year_built", "floor_count", "air_temperature", "cloud_coverage", "dew_temperature",
"precip_depth_1_hr", "sea_level_pressure", "wind_direction", "wind_speed", "day_of_week", "month", "day", "hour"]

conversion_dict = {
    "time": "timestamp",
    "temperature_2m": "air_temperature",
    "cloudcover": "cloud_coverage",
    "dewpoint_2m": "dew_temperature",
    "precipitation": "precip_depth_1_hr",
    "pressure_msl": "sea_level_pressure",
    "windspeed_10m": "wind_speed",
    "winddirection_10m": "wind_direction",
}

with open('models.pickle', 'rb') as f:
    models: list[HistGradientBoostingRegressor] = pickle.load(f)

with open('encoder.pickle', 'rb') as f:
    encoder: OrdinalEncoder = pickle.load(f)

def get_historical_weather(lat, long, days=1):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    params = dict(
        latitude=lat,
        longitude=long,
        hourly=",".join(hourly),
        windspeed_unit="ms",
        timeformat="unixtime",
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
    )
    param_str = "&".join(f"{k}={v}" for k, v in params.items())
    res = requests.get(f"{URL}?{param_str}")
    res.raise_for_status()
    res_json = res.json()
    df = pd.DataFrame(res_json["hourly"])
    df.rename(columns=conversion_dict, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit="s")
    df['cloud_coverage'] = df['cloud_coverage'] / 100 * 8  # percentage to oktal (?)
    return df


def get_historical_predictions(lat, long, square_feet, floor_count, year_built, primary_use):
    df = get_historical_weather(lat, long)
    df["square_feet"] = square_feet
    df["floor_count"] = floor_count
    df["year_built"] = year_built
    df["primary_use"] = primary_use
    df["day_of_week"] = df["timestamp"].dt.day_of_week
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month
    df["hour"] = df["timestamp"].dt.hour

    transformed = encoder.transform(df.primary_use.to_numpy().reshape(-1, 1))
    ohe_df = pd.DataFrame(transformed, columns=["primary_use_ordinal"])
    df = pd.concat([df, ohe_df], axis=1)
    eval_df = df[fields]

    nrows, ncols = len(models), 1
    fig, ax = plt.subplots(nrows, ncols, figsize=(14,8))

    for i, meter, model in zip(range(len(models)), meters, models):
        pred_meter_readings = model.predict(eval_df)
        pred_meter_readings = np.clip(pred_meter_readings, 0, None)
        cax = plt.subplot(nrows, ncols, i + 1)
        cax.plot(df['timestamp'].values, pred_meter_readings)
        cax.xaxis.set_major_locator(plt.MaxNLocator(3))
        cax.set_title('Meter: {}, Pred'.format(meter), fontsize=10)

    plt.tight_layout()
    plt.show()


get_historical_predictions(33.77,  -84.3956,
square_feet=8000,
floor_count=None,
year_built=None,
primary_use="Lodging/residential"
)
