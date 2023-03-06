"""The app module, containing the app factory function."""
import json
import logging
import sys
import os
from flask import Flask, jsonify
from flask_swagger import swagger
from app.extensions import cors, database, mqtt


def create_app(config_object):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)
    configure_swagger_spec(app)
    create_dev_mode_user()

    from app.services.schedule_irrigation_service import ScheduleIrrigationService

    ScheduleIrrigationService.verify_schedule()
    ScheduleIrrigationService.worker_schedule()

    return app


def register_extensions(app):
    """Register Flask extensions."""
    database.init_app(app)
    cors.init_app(app)
    mqtt.init_app(app)
    return None


def create_dev_mode_user():
    from app.controllers.user_controller import users
    from app.constants.dev_mode_user import dev_mode_user

    dev_mode_user_already_created = users.find_one({"email": dev_mode_user["email"]})
    if dev_mode_user_already_created is None:
        users.insert_one(dev_mode_user)
        dev_mode_user["password"] = os.getenv("DEV_MODE_USER_PASSWORD")
        print(json.dumps(dev_mode_user, indent=4, sort_keys=True, ensure_ascii=False, default=str))




def register_blueprints(app):
    """Register Flask blueprints."""
    from .routes.users import users_bp
    from .routes.irrigation_zones import irrigation_zones_bp
    from .routes.cultures import cultures_bp
    from .routes.sensors import sensors_bp
    from .routes.swagger import swagger_bp
    from .routes.sensor_types import sensor_types_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(irrigation_zones_bp, url_prefix="/irrigation-zones")
    app.register_blueprint(cultures_bp, url_prefix="/cultures")
    app.register_blueprint(sensors_bp, url_prefix="/sensors")
    app.register_blueprint(swagger_bp)
    app.register_blueprint(sensor_types_bp, url_prefix="/sensor-types")

    return None


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def configure_swagger_spec(app):
    def swagger_spec():
        specs = swagger(app)

        specs["info"]["version"] = "0.0.1"
        specs["info"]["title"] = "PC2I Platform"

        return jsonify(specs)

    app.add_url_rule("/specs", view_func=swagger_spec)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("pc2i/irrigation-zones/#")


@mqtt.on_subscribe()
def handle_subscribe(client, userdata, mid, granted_qos):
    print("Subscription id {} granted with qos {}.".format(mid, granted_qos))


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(topic=message.topic, payload=message.payload.decode())
    print(data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    if level == MQTT_LOG_ERR:
        print("Error: {}".format(buf))
