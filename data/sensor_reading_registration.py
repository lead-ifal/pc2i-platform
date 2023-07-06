from connection import database
import pandas as pd
import requests
import os
import dotenv
from bson import ObjectId

dotenv.load_dotenv(dotenv.find_dotenv())

sensors_table = database["sensors"]
sensor_reading_table = database["sensors_readings"]
culture_table = database["cultures"]


class SensorReadingRegistration:
    def TrainCreate():
        train = pd.read_csv("csv_files/Train.csv")
        sensor_names = train.columns.tolist()
        date = train["timestamp"]
        sensor_names.remove("timestamp")

        for sensor_name in sensor_names:
            values = train[sensor_name].tolist()
            sensor = sensors_table.find_one({"name": sensor_name})
            linha = 0
            for value in values:
                sensor_id = sensor["_id"]
                url = (
                    os.getenv("SENSOR_URL")
                    + "/"
                    + str(sensor_id)
                    + "/"
                    + str(value)
                    + "/"
                    + date[linha]
                )
                requests.post(url)
                linha = linha + 1

    def ContextDataPeanutCreate():
        peanut_1_id = ObjectId(os.getenv("PEANUT_1_ID"))
        peanut_2_id = ObjectId(os.getenv("PEANUT_2_ID"))
        peanut_3_id = ObjectId(os.getenv("PEANUT_3_ID"))
        data_peanuts = pd.read_csv("csv_files/Context_Data_Peanuts.csv")
        sensor_names = data_peanuts.columns.tolist()
        date = data_peanuts["Date"]
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
            linha = 0
            for value in values:

                url = (
                    os.getenv("SENSOR_URL")
                    + "/"
                    + str(sensor_1_id)
                    + "/"
                    + str(value)
                    + "/"
                    + str(date[linha])
                )
                requests.post(url)
                url = (
                    os.getenv("SENSOR_URL")
                    + "/"
                    + str(sensor_2_id)
                    + "/"
                    + str(value)
                    + "/"
                    + str(date[linha])
                )
                requests.post(url)
                url = (
                    os.getenv("SENSOR_URL")
                    + "/"
                    + str(sensor_3_id)
                    + "/"
                    + str(value)
                    + "/"
                    + str(date[linha])
                )
                requests.post(url)
                linha = linha + 1

    def ContextDataMaizeCreate():
        maize_id = ObjectId(os.getenv("MAIZE_ID"))
        data_maize = pd.read_csv("csv_files/Context_Data_Maize.csv")
        sensor_names = data_maize.columns.tolist()
        context = []

        url = os.getenv("CULTURE_URL") + "/" + str(maize_id)

        for index, row in data_maize.iterrows():
            context_row = []

            for column_name, value in row.items():
                context_row.append({column_name: str(value)})
            context.append(context_row)

        culture = culture_table.find_one({"_id": ObjectId(maize_id)})

        culture = {
            "irrigation_zone_id": str(culture["irrigation_zone_id"]),
            "name": culture["name"],
            "type": culture["type"],
            "planting_date": str(culture["planting_date"]),
            "coefficient_et": str(culture["coefficient_et"]),
            "phase": culture["phase"],
            "geographic_coordinates": culture["geographic_coordinates"],
            "context": context,
        }

        requests.patch(url, json=culture)
