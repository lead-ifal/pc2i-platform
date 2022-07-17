from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class schedule_irrigation(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    irrigation_zone_id: str
    liters_of_water: int
    day: str
    time: int
