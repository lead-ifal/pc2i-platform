from flask import request, Response
from bson import ObjectId
from datetime import datetime
from app.extensions import database
from app.controllers.global_controller import GlobalController
from app.middlewares.access_control import access_control
from app.middlewares.check_mongodb_id import check_mongodb_id
from app.middlewares.has_token import has_token
from app.models.culture import Culture
from sklearn.metrics import r2_score
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.svm import SVR
import numpy as np
from keras.models import Sequential
from app.constants.status_code import (
    HTTP_BAD_REQUEST_CODE,
    HTTP_CREATED_CODE,
    HTTP_SUCCESS_CODE,
    HTTP_NOT_FOUND_CODE,
    HTTP_SERVER_ERROR_CODE,
)
from app.constants.response_messages import (
    ERROR_MESSAGE,
    SUCCESS_MESSAGE,
    CULTURE_NOT_FOUND_MESSAGE,
    INTERNAL_SERVER_ERROR_MESSAGE,
)
from app.constants.required_params import required_params
from typing import Collection

cultures: Collection = database.db.cultures
irrigation_zones: Collection = database.db.irrigation_zones


class CultureController:
    @has_token
    def create():
        body = {**request.form.to_dict(), **request.files.to_dict()}
        params = required_params["cultures"]["create"]
        includes_params = GlobalController.includes_all_required_params(params, body)

        try:
            if includes_params:
                body["irrigation_zone_id"] = ObjectId(body["irrigation_zone_id"])
                body["planting_date"] = datetime.fromisoformat(body["planting_date"])
                body["geographic_coordinates"] = {
                    "type": "Point",
                    "coordinates": body["geographic_coordinates"],
                }

                if "harvest_date" in body:
                    body["harvest_date"] = datetime.fromisoformat(body["harvest_date"])

                culture = Culture(**body)
                culture_data = culture.dict(exclude_none=True)
                filter = {"_id": body["irrigation_zone_id"]}
                irrigation_zone_exists = irrigation_zones.count(filter) == 1

                if irrigation_zone_exists:
                    if "image" in body:
                        now = datetime.now().strftime("%Y%m%d%H%M%S")
                        image_filename = "{}-{}".format(now, body["image"].filename)
                        culture_data["image"] = image_filename

                        database.save_file(image_filename, body["image"])

                    cultures.insert_one(culture_data)

                    irrigation_zones.find_one_and_update(
                        {"_id": culture_data["irrigation_zone_id"]},
                        {"$push": {"cultures": culture_data["_id"]}},
                    )

                    return GlobalController.generate_response(
                        HTTP_CREATED_CODE, SUCCESS_MESSAGE, culture_data
                    )

            raise Exception()

        except:
            return GlobalController.generate_response(
                HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE
            )

    @access_control(levels=2)
    @check_mongodb_id
    @has_token
    def delete(culture_id):
        try:
            culture = cultures.find_one_and_delete({"_id": ObjectId(culture_id)})

            irrigation_zones.find_one_and_update(
                {"_id": culture["irrigation_zone_id"]},
                {"$pull": {"cultures": culture["_id"]}},
            )
            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, culture_id
            )

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @access_control(levels=2)
    @check_mongodb_id
    @has_token
    def update(culture_id):
        body = {**request.form.to_dict(), **request.files.to_dict()}
        params = required_params["cultures"]["create"]
        includes_params = GlobalController.includes_all_required_params(params, body)

        try:
            if includes_params:
                body["planting_date"] = datetime.fromisoformat(body["planting_date"])
                body["geographic_coordinates"] = {
                    "type": "Point",
                    "coordinates": body["geographic_coordinates"],
                }

                if "harvest_date" in body:
                    body["harvest_date"] = datetime.fromisoformat(body["harvest_date"])

                body["irrigation_zone_id"] = ObjectId(body["irrigation_zone_id"])
                culture = Culture(**body)
                culture_data = culture.dict(exclude_none=True)
                if "image" in body:
                    now = datetime.now().strftime("%Y%m%d%H%M%S")
                    image_filename = "{}-{}".format(now, body["image"].filename)
                    culture_data["image"] = image_filename
                    database.save_file(image_filename, body["image"])
                cultures.find_one_and_update(
                    {"_id": ObjectId(culture_id)}, {"$set": culture_data}
                )
                return GlobalController.generate_response(
                    HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, culture_data
                )

            raise Exception()

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @check_mongodb_id
    def list(irrigation_zone_id):
        try:
            culture_list = cultures.find(
                {"irrigation_zone_id": ObjectId(irrigation_zone_id)}
            )
            data = []

            for culture in culture_list:
                data.append(culture)

            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data
            )

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    @check_mongodb_id
    def show(culture_id):
        try:
            data = None

            data = cultures.find_one({"_id": ObjectId(culture_id)})

            if data != None:
                return GlobalController.generate_response(
                    HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data
                )

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    def linear_regression(features, target):
        (
            features_train,
            features_test,
            target_train,
            target_test,
        ) = train_test_split(features, target, test_size=0.3)

        model = LinearRegression()

        model.fit(features_train, target_train)

        predictions = model.predict(features_test)

        accuracy = r2_score(target_test, predictions)

        return accuracy

    def create_dataset(dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - look_back - 1):
            a = dataset[i : (i + look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return np.array(dataX), np.array(dataY)

    def lstm(dataset):
        train, test = train_test_split(dataset, test_size=0.3)
        scaler = MinMaxScaler(feature_range=(0, 1))
        train = scaler.fit_transform(np.array(train).reshape(-1, 1))
        test = scaler.transform(np.array(test).reshape(-1, 1))

        look_back = 18
        trainX, trainY = CultureController.create_dataset(train, look_back)
        testX, testY = CultureController.create_dataset(test, look_back)

        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        model = Sequential()
        model.add(LSTM(4, input_shape=(1, 18)))
        model.add(Dense(1))
        model.compile(loss="mean_squared_error", optimizer="adam")
        model.fit(trainX, trainY, epochs=5, batch_size=1, verbose=2)

        predictions = model.predict(testX)

        accuracy = r2_score(testY, predictions)

        return accuracy

    def predict(culture_id):
        maize = culture_id
        context = cultures.find_one({"_id": ObjectId(maize)})["context"]

        train = pd.read_csv("data/csv_files/Train.csv")
        train = train.drop(
            [
                "Soil humidity 2",
                "Irrigation field 2",
                "Soil humidity 3",
                "Irrigation field 3",
                "Soil humidity 4",
                "Irrigation field 4",
            ],
            axis=1,
        )

        readings = []
        for index, row in train.iterrows():
            readings_row = {}

            for column_name, value in row.items():
                readings_row[column_name] = str(value)
            readings.append(readings_row)

        for reading in readings:
            data = datetime.strptime(reading["timestamp"], "%Y-%m-%d %H:%M:%S")
            for value in context:
                date = datetime.strptime(value["Date"], "%d-%b")
                year = "2019"
                date_with_year = date.replace(year=int(year))

                formatted_date = date_with_year.strftime("%Y-%m-%d")
                if formatted_date == str(data.date()):
                    reading.update(value)

        readings_lenght = len(readings)
        index = 0
        while index < readings_lenght:
            reading = readings[index]
            for value in reading:
                if reading[value] == "nan":
                    readings.remove(reading)
                    index = index - 1
                    readings_lenght = readings_lenght - 1
                    break
            index = index + 1

        data = pd.DataFrame(readings)

        data = data.drop(
            [
                "Date",
                "timestamp",
            ],
            axis=1,
        )

        features = data[
            [
                "Soil humidity 1",
                "Irrigation field 1",
                "Air temperature (C)",
                "Air humidity (%)",
                "Pressure (KPa)",
                "Wind speed (Km/h)",
                "Wind gust (Km/h)",
                "Wind direction (Deg)",
                "Min_Temp",
                "Max_Temp",
                "Humidity",
                "Wind_Speed",
                "Solar_Irradiance",
                "Sun",
                "Kc",
                "ETc",
                "ETo",
                "Rainfall",
            ]
        ]

        target_1day = data["Water_Need_1day"]
        target_2days = data["Water_Need_2days"]
        target_3days = data["Water_Need_3days"]

        r2_score_1day_lr = CultureController.linear_regression(features, target_1day)
        r2_score_2days_lr = CultureController.linear_regression(features, target_2days)
        r2_score_3days_lr = CultureController.linear_regression(features, target_3days)

        lstm_dataset_1 = data[
            [
                "Soil humidity 1",
                "Irrigation field 1",
                "Air temperature (C)",
                "Air humidity (%)",
                "Pressure (KPa)",
                "Wind speed (Km/h)",
                "Wind gust (Km/h)",
                "Wind direction (Deg)",
                "Min_Temp",
                "Max_Temp",
                "Humidity",
                "Wind_Speed",
                "Solar_Irradiance",
                "Sun",
                "Kc",
                "ETc",
                "ETo",
                "Rainfall",
                "Water_Need_1day",
            ]
        ]
        lstm_dataset_2 = data[
            [
                "Soil humidity 1",
                "Irrigation field 1",
                "Air temperature (C)",
                "Air humidity (%)",
                "Pressure (KPa)",
                "Wind speed (Km/h)",
                "Wind gust (Km/h)",
                "Wind direction (Deg)",
                "Min_Temp",
                "Max_Temp",
                "Humidity",
                "Wind_Speed",
                "Solar_Irradiance",
                "Sun",
                "Kc",
                "ETc",
                "ETo",
                "Rainfall",
                "Water_Need_2days",
            ]
        ]
        lstm_dataset_3 = data[
            [
                "Soil humidity 1",
                "Irrigation field 1",
                "Air temperature (C)",
                "Air humidity (%)",
                "Pressure (KPa)",
                "Wind speed (Km/h)",
                "Wind gust (Km/h)",
                "Wind direction (Deg)",
                "Min_Temp",
                "Max_Temp",
                "Humidity",
                "Wind_Speed",
                "Solar_Irradiance",
                "Sun",
                "Kc",
                "ETc",
                "ETo",
                "Rainfall",
                "Water_Need_3days",
            ]
        ]

        r2_score_1day_lstm = CultureController.lstm(lstm_dataset_1)
        r2_score_2days_lstm = CultureController.lstm(lstm_dataset_2)
        r2_score_3days_lstm = CultureController.lstm(lstm_dataset_3)

        names = [
            "LR - 1 Dia",
            "LSTM - 1 Dia",
            "LR - 2 Dias",
            "LSTM - 2 Dias",
            "LR - 3 Dias",
            "LSTM - 3 Dias",
        ]
        values = [
            r2_score_1day_lr,
            r2_score_1day_lstm,
            r2_score_2days_lr,
            r2_score_2days_lstm,
            r2_score_3days_lr,
            r2_score_3days_lstm,
        ]

        colors = ["blue", "red"]

        plt.figure(figsize=(10, 6))
        plt.bar(names, values, color=colors)
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format="png")
        plt.close()

        return Response(img_buffer.getvalue(), content_type="image/png")
