from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId
from app.extensions import database
from typing import Collection

irrigation_zones: Collection = database.db.irrigation_zones


class IrrigationZone(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    user_id: ObjectId
    cultures: Optional[list]
    schedules: Optional[list]
    name: str
    description: str
    size: float
    irrigation_type: int

    def get_irrigation_zone_by_id(id):
        irrigation_zone = irrigation_zones.find_one({"_id": ObjectId(id)})
        return irrigation_zone

    def get_irrigation_zone_by_entity_id(id):
        irrigation_zone = irrigation_zones.find_one(
            {
                "$or": [
                    {"cultures": ObjectId(id)},
                    {"schedules": ObjectId(id)},
                ]
            }
        )
        return irrigation_zone

    class Config:
        arbitrary_types_allowed = True
