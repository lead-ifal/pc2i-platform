from bson import ObjectId
from flask import request
from typing import Collection
from app.extensions import database, mqtt
from app.middlewares.check_mongodb_id import check_mongodb_id
from app.middlewares.has_token import has_token
from app.models.sensor import Sensor
from app.controllers.global_controller import GlobalController
from app.constants.status_code import (
    HTTP_BAD_REQUEST_CODE,
    HTTP_CREATED_CODE,
    HTTP_NOT_FOUND_CODE,
    HTTP_SUCCESS_CODE,
    HTTP_SERVER_ERROR_CODE,
)
from app.constants.response_messages import (
    ERROR_MESSAGE,
    READINGS_NOT_FOUND_MESSAGE,
    SUCCESS_MESSAGE,
    INTERNAL_SERVER_ERROR_MESSAGE,
)
from app.constants.required_params import required_params
from app.models.sensor_reading import SensorReading

cultures: Collection = database.db.cultures
sensors: Collection = database.db.sensors
sensors_readings: Collection = database.db.sensors_readings


class SensorController:
    @has_token
    def create():
        body = request.get_json()
        params = required_params["sensors"]["create"]
        includes_params = GlobalController.includes_all_required_params(params, body)

        try:
            if includes_params:
                body["culture_id"] = ObjectId(body["culture_id"])
                body["type"] = ObjectId(body["type"])
                sensor = Sensor(**body)
                result = sensors.insert_one(sensor.dict(exclude_none=True))
                sensor_data = sensor.dict(exclude_none=True)
                sensor_data["_id"] = result.inserted_id

                return GlobalController.generate_response(
                    HTTP_CREATED_CODE, SUCCESS_MESSAGE, sensor_data
                )

            raise Exception()

        except:
            return GlobalController.generate_response(
                HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE
            )

    @check_mongodb_id
    def list(irrigation_zone_id):

        try:
            sensors_zone_list = sensors.find(
                {"irrigation_zone_id": ObjectId(irrigation_zone_id)}
            )
            data = []
            for sensor in sensors_zone_list:
                data.append(sensor)

            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data
            )
        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, ERROR_MESSAGE
            )

    @has_token
    def publish(sensor_id, value):
        topic = "pc2i/" + sensor_id
        mqtt.subscribe(topic)
        publish_result = mqtt.publish(topic, value)
        print("teste")
        print(publish_result)
        return GlobalController.generate_response(
            HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, "publish_result"
        )

    @mqtt.on_message()
    def handle_messages(client, userdata, message):
        body = {
            "sensor_id": message.topic.replace("pc2i/", ""),
            "value": message.payload.decode(),
        }
        body["sensor_id"] = ObjectId(body["sensor_id"])
        sensor_reading = SensorReading(**body)
        result = sensors_readings.insert_one(sensor_reading.dict(exclude_none=True))
        sensor_reading_data = sensor_reading.dict(exclude_none=True)
        sensor_reading_data["_id"] = result.inserted_id

        if sensor_reading_data["_id"]:
            return GlobalController.generate_response(
                HTTP_CREATED_CODE, SUCCESS_MESSAGE, sensor_reading_data
            )

        raise Exception()

    def list_readings():
        ASCENDING = 1
        DESCENDING = -1
        irrigation_zone_id = request.args.get("irrigation-zone")
        filter = request.args.get("filter")
        sensor_id = request.args.get("sensor")
        data = []

        try:
            db_query = {"filter": {}, "limit": 1000, "sort": {"_id": ASCENDING}}

            # Buscar leituras por zona de irrigacao
            if irrigation_zone_id != None:
                isInvalidId = (
                    GlobalController.is_valid_mongodb_id(irrigation_zone_id) == False
                )

                if isInvalidId:
                    return GlobalController.generate_response(
                        HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE
                    )

                sensor_ids = []
                match_irrigation_zone = {
                    "irrigation_zone_id": ObjectId(irrigation_zone_id)
                }
                lookup_sensors = {
                    "from": "sensors",
                    "localField": "_id",
                    "foreignField": "culture_id",
                    "as": "sensors",
                }
                group_ids = {"_id": None, "sensor_ids": {"$push": "$sensors._id"}}
                results = cultures.aggregate(
                    [
                        {"$match": match_irrigation_zone},
                        {"$lookup": lookup_sensors},
                        {"$group": group_ids},
                        {"$unwind": "$sensor_ids"},
                    ]
                )

                for result in results:
                    sensor_ids = result["sensor_ids"]

                if len(sensor_ids) == 0:
                    return GlobalController.generate_response(
                        HTTP_NOT_FOUND_CODE, READINGS_NOT_FOUND_MESSAGE
                    )

                db_query["filter"]["sensor_id"] = {"$in": sensor_ids}

            # Buscar leituras por sensor
            if sensor_id != None:
                isInvalidId = GlobalController.is_valid_mongodb_id(sensor_id) == False

                if isInvalidId:
                    return GlobalController.generate_response(
                        HTTP_NOT_FOUND_CODE, READINGS_NOT_FOUND_MESSAGE
                    )

                db_query["filter"]["sensor_id"] = ObjectId(sensor_id)

            # Buscar a ultima leitura
            if filter != None:
                if filter == "last":
                    db_query["limit"] = 1
                    db_query["sort"] = {"date": DESCENDING}

            lookup_sensors = {
                "from": "sensors",
                "localField": "sensor_id",
                "foreignField": "_id",
                "as": "sensor",
            }
            lookup_cultures = {
                "from": "cultures",
                "localField": "sensor.culture_id",
                "foreignField": "_id",
                "as": "culture",
            }
            fields = {
                "value": 1,
                "sensor_id": 1,
                "sensor_type": "$sensor.type",
                "irrigation_zone_id": "$culture.irrigation_zone_id",
            }
            readings = sensors_readings.aggregate(
                [
                    {"$match": db_query["filter"]},
                    {"$lookup": lookup_sensors},
                    {"$unwind": "$sensor"},
                    {"$lookup": lookup_cultures},
                    {"$unwind": "$culture"},
                    {"$sort": db_query["sort"]},
                    {"$limit": db_query["limit"]},
                    {"$project": fields},
                ]
            )

            for reading in readings:
                data.append(reading)

            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data
            )
        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )
