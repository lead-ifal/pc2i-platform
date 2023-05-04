import json
from bson import ObjectId
from datetime import datetime


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        elif isinstance(o, datetime):
            return o.isoformat()

        else:
            return json.JSONEncoder.default(self, o)
