from connection import database
import pandas as pd
import requests
import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

sensors_table = database["sensors"]
sensor_types_table = database["sensor_types"]


class SensorRegistration:
    def TrainCreate():
        url = os.getenv("URL")
        peanut_1_id = os.getenv("PEANUT_1_ID")
        peanut_2_id = os.getenv("PEANUT_2_ID")
        peanut_3_id = os.getenv("PEANUT_3_ID")
        maize_id = os.getenv("MAIZE_ID")
        sensor = {}
        train = pd.read_csv("csv_files\Train.csv")
        sensor_names = train.columns.tolist()
        sensor_names.remove("timestamp")
        for sensor_name in sensor_names:
            sensor_type = sensor_types_table.find_one({"type": sensor_name})
            sensor_type_id = sensor_type["_id"]
            sensor["type"] = str(sensor_type_id)
            sensor["name"] = str(sensor_name)
            if (
                sensor["name"] == "Soil humidity 2"
                or sensor["name"] == "Irrigation field 2"
            ):
                sensor["culture_id"] = peanut_1_id
            elif (
                sensor["name"] == "Soil humidity 3"
                or sensor["name"] == "Irrigation field 3"
            ):
                sensor["culture_id"] = peanut_2_id
            elif (
                sensor["name"] == "Soil humidity 4"
                or sensor["name"] == "Irrigation field 4"
            ):
                sensor["culture_id"] = peanut_3_id
            else:
                sensor["culture_id"] = maize_id

            requests.post(url, json=sensor)

    def ContextDataPeanutCreate():
        url = os.getenv("URL")
        peanut_1_id = os.getenv("PEANUT_1_ID")
        peanut_2_id = os.getenv("PEANUT_2_ID")
        peanut_3_id = os.getenv("PEANUT_3_ID")
        sensor = {}
        data_peanuts = pd.read_csv("csv_files\Context_Data_Peanuts.csv")
        sensor_names = data_peanuts.columns.tolist()
        sensor_names.remove("Date")
        for sensor_name in sensor_names:
            sensor_type = sensor_types_table.find_one({"type": sensor_name})
            sensor_type_id = sensor_type["_id"]
            sensor["type"] = str(sensor_type_id)
            sensor["name"] = str(sensor_name)
            sensor["culture_id"] = peanut_1_id

            requests.post(url, json=sensor)
            sensor["culture_id"] = peanut_2_id
            requests.post(url, json=sensor)
            sensor["culture_id"] = peanut_3_id
            requests.post(url, json=sensor)

    def ContextDataMaizeCreate():
        url = os.getenv("URL")
        maize_id = os.getenv("MAIZE_ID")
        sensor = {}
        data_maize = pd.read_csv("csv_files\Context_Data_Maize.csv")
        sensor_names = data_maize.columns.tolist()
        sensor_names.remove("Date")
        for sensor_name in sensor_names:
            sensor_type = sensor_types_table.find_one({"type": sensor_name})
            sensor_type_id = sensor_type["_id"]
            sensor["type"] = str(sensor_type_id)
            sensor["name"] = str(sensor_name)
            sensor["culture_id"] = maize_id

            requests.post(url, json=sensor)
