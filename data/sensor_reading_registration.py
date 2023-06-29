from connection import database
import pandas as pd
import requests
import os
import dotenv
from bson import ObjectId


dotenv.load_dotenv(dotenv.find_dotenv())

sensors_table = database["sensors"]
sensor_reading_table = database["sensors_readings"]


class SensorReadingRegistration:
    def TrainCreate():
        train = pd.read_csv("csv_files/Train.csv")
        sensor_names = train.columns.tolist()
        sensor_names.remove("timestamp")

        for sensor_name in sensor_names:
            values = train[sensor_name].tolist()
            sensor = sensors_table.find_one({"name": sensor_name})
            for value in values:
                sensor_id = sensor["_id"]
                url = os.getenv("URL") + "/" + str(sensor_id) + "/" + str(value)
                requests.post(url)

    def ContextDataPeanutCreate():
        peanut_1_id = ObjectId(os.getenv("PEANUT_1_ID"))
        peanut_2_id = ObjectId(os.getenv("PEANUT_2_ID"))
        peanut_3_id = ObjectId(os.getenv("PEANUT_3_ID"))
        data_peanuts = pd.read_csv("csv_files/Context_Data_Peanuts.csv")
        sensor_names = data_peanuts.columns.tolist()
        sensor_names.remove("Date")

        for sensor_name in sensor_names:
            values = data_peanuts[sensor_name].tolist()
            sensor_1 = sensors_table.find_one(
                {"name": sensor_name, "culture_id": peanut_1_id}
            )
            sensor_2 = sensors_table.find_one(
                {"name": sensor_name, "culture_id": peanut_2_id}
            )
            sensor_3 = sensors_table.find_one(
                {"name": sensor_name, "culture_id": peanut_3_id}
            )
            sensor_1_id = sensor_1["_id"]
            sensor_2_id = sensor_2["_id"]
            sensor_3_id = sensor_3["_id"]
            for value in values:
                url = os.getenv("URL") + "/" + str(sensor_1_id) + "/" + str(value)
                requests.post(url)
                url = os.getenv("URL") + "/" + str(sensor_2_id) + "/" + str(value)
                requests.post(url)
                url = os.getenv("URL") + "/" + str(sensor_3_id) + "/" + str(value)
                requests.post(url)

    def ContextDataMaizeCreate():
        maize_id = ObjectId(os.getenv("MAIZE_ID"))
        data_maize = pd.read_csv("csv_files/Context_Data_Maize.csv")
        sensor_names = data_maize.columns.tolist()
        sensor_names.remove("Date")

        for sensor_name in sensor_names:
            values = data_maize[sensor_name].tolist()
            sensor = sensors_table.find_one(
                {"name": sensor_name, "culture_id": maize_id}
            )
            sensor_id = sensor["_id"]
            for value in values:
                url = os.getenv("URL") + "/" + str(sensor_id) + "/" + str(value)
                requests.post(url)
