import numpy as np
import pandas as pd
import requests
import pickle
import datetime
import utils
from flask import Flask, request
from flask_caching import Cache
from flask_cors import CORS
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import HistGradientBoostingRegressor

app = Flask(__name__)
CORS(app)
app.config["CACHE_TYPE"] = "SimpleCache"
cache = Cache(app)

with open('../prediction/models.pickle', 'rb') as f:
    models: list[HistGradientBoostingRegressor] = pickle.load(f)

with open('../prediction/encoder.pickle', 'rb') as f:
    encoder: OrdinalEncoder = pickle.load(f)


def get_historical_predictions(lat, long, square_feet, floor_count, year_built, primary_use):
    df = utils.get_historical_weather(lat, long)
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
    eval_df = df[utils.FIELDS]

    data = {
        "timestamp": (df["timestamp"].astype(int) / 10 ** 9).astype(int).tolist()
    }
    for i, meter_name, model in zip(range(len(models)), utils.METERS, models):
        pred_meter_readings = model.predict(eval_df)
        pred_meter_readings = np.clip(pred_meter_readings, 0, None)
        data[meter_name] = pred_meter_readings.tolist()
    return data

@cache.cached(timeout=3600)
def precisely_auth():
    return utils.get_precisely_auth()


def address_details(address):
    auth = precisely_auth()
    return utils.precisely_get_address_details(address, auth)
    



@app.route('/')
def index():
    precisely_auth()
    return 'Hello'



@app.route('/query', methods=["GET", "POST"])
def query():
    req_json = request.get_json()
    long = req_json.get("long")
    lat = req_json.get("lat")
    address = req_json.get("address")
    details, is_fetched_successfully = address_details(address)
    predictions = get_historical_predictions(
        lat=lat,
        long=long,
        **details,
    )
    res = dict(
        predictions=predictions,
        buildingData=details,
        foundBuildingData=is_fetched_successfully,
    )
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
