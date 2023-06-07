from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId


class IrrigationZone(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    user_id: ObjectId
    cultures: list
    schedules: list
    name: str
    description: str
    size: float
    irrigation_type: int

    class Config:
        arbitrary_types_allowed = True
