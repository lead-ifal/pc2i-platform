from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime

from .objectid import PydanticObjectId

class Cultivation(BaseModel):
    name: str
    type: str
    planting_date: datetime
    harvest_date: datetime
    culture_ratio: int
    cultivation_phase: str
    soil_characteristics: int
    location: str
    change_date_phase: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        dict_encoders = {str: lambda x: PydanticObjectId(x) if PydanticObjectId.is_valid(x) else x}
        json_encoders = {PydanticObjectId: str}

    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    def to_json(self):
        return jsonable_encoder(self, by_alias=True, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data