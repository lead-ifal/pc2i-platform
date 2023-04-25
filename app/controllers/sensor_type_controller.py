from typing import Collection
from flask import request
from app.controllers.global_controller import GlobalController
from app.middlewares.has_token import has_token
from app.extensions import database
from app.constants.required_params import required_params
from app.models.sensor_type import SensorType
from app.constants.status_code import (
    HTTP_BAD_REQUEST_CODE,
    HTTP_CREATED_CODE,
    HTTP_SUCCESS_CODE,
    HTTP_SERVER_ERROR_CODE,
)
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE

sensor_types: Collection = database.db.sensor_types


class SensorTypeConstroller:
    @has_token
    def create():
        """
        Registration of sensor types
        ---
        tags:
          - Sensor Types
        parameters:
          - name: token
            in: header
            description: Authentication key
          - name: data
            description: Registered sensor type
            in: body
            schema:
              properties:
                type:
                  required: true
                  description: Sensor type
                  type: string
        responses:
          201:
            description: Successfully Created
          400:
            description: Invalid data
          401:
            description: Unauthorized
          500:
            description: Internal server error
        """
        body = request.get_json()
        params = required_params["sensor_types"]["create"]
        includes_params = GlobalController.includes_all_required_params(params, body)

        try:

            if includes_params:
                sensor_type = SensorType(**body)
                result = sensor_types.insert_one(sensor_type.dict(exclude_none=True))
                sensor_type_data = sensor_type.dict(exclude_none=True)
                sensor_type_data["_id"] = result.inserted_id

                return GlobalController.generate_response(
                    HTTP_CREATED_CODE, SUCCESS_MESSAGE, sensor_type_data
                )

            else:
                return GlobalController.generate_response(
                    HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE
                )

        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, ERROR_MESSAGE
            )

    def list():
        """
        List of sensor types
        ---
        tags:
          - Sensor Types
        responses:
          200:
            description: Success
            schema:
              properties:
                message:
                  type: string
                data:
                  type: array
                  items:
                    schema:
                      id: Sensor Type
                      properties:
                        _id:
                          description: MongoDB ObjectID for sensor type
                          type: string
                        type:
                          description: Sensor type
                          type: string
          500:
            description: Internal server error
        """
        try:

            sensor_types_list = list(sensor_types.find({}))

            return GlobalController.generate_response(
                HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, sensor_types_list
            )

        except:

            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, ERROR_MESSAGE
            )
