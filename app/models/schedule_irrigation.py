from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class ScheduleIrrigation(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    irrigation_zone_id: str
    liters_of_water: int
    days: list
    time: int
    moment_of_activation: float
