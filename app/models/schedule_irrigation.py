from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class ScheduleIrrigation(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    irrigation_zone_id: ObjectId
    liters_of_water: int
    days: list
    time: str
    duration: str

    class Config:
        arbitrary_types_allowed = True
