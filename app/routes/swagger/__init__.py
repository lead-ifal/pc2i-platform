from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_UI_URL = "/api/docs"
SWAGGER_SPECS_URL = "http://0.0.0.0:1026/specs"


swagger_bp = get_swaggerui_blueprint(
    SWAGGER_UI_URL,
    SWAGGER_SPECS_URL,
    config={"app_name": "PC2I Platform"},
)
