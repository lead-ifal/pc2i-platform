# -*- coding: utf-8 -*-
"""Create an application instance."""
from config import Config
from app.app import create_app

app = create_app(Config)
app.run(host='0.0.0.0', port='1026')
