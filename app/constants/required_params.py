required_params = {
    "users": {
        "create": ["name", "email", "password"],
        "read": ["email", "password"],
        "update": ["name", "email", "password", "new_password"],
    },
    "irrigation_zones": {
        "create": ["user_id", "name", "description", "size", "irrigation_type"],
        "schedule": [
            "irrigation_zone_id",
            "liters_of_water",
            "time",
            "days",
            "duration",
        ],
    },
    "cultures": {
        "create": [
            "irrigation_zone_id",
            "name",
            "type",
            "planting_date",
            "phase",
            "geographic_coordinates",
        ],
    },
    "sensors": {"create": ["culture_id", "name"], "read": ["culture_id"]},
    "sensor_types": {"create": ["type"]},
}
