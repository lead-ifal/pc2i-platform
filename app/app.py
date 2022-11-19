"""The app module, containing the app factory function."""
import logging
import sys


from app.extensions import cors, database, mqtt
from flask import Flask


def create_app(config_object):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)
    #from app.services.schedule_irrigation_service import ScheduleIrrigationService
    #ScheduleIrrigationService.verify_schedule()
    #ScheduleIrrigationService.worker_schedule()
    return app


def register_extensions(app):
    """Register Flask extensions."""
    database.init_app(app)
    cors.init_app(app)
    mqtt.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    from .routes.users import users_bp
    from .routes.irrigation_zones import irrigation_zones_bp
    from .routes.cultures import cultures_bp
    from .routes.sensors import sensors_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(irrigation_zones_bp, url_prefix="/irrigation-zones")
    app.register_blueprint(cultures_bp, url_prefix="/cultures")
    app.register_blueprint(sensors_bp, url_prefix="/sensors")
    return None


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


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
<<<<<<< HEAD
        print("Error: {}".format(buf))
=======
        print('Error: {}'.format(buf))
>>>>>>> 7aeff3d (temp: desativacao da verificacao de irrigacao)
