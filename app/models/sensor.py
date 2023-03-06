from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId


class Sensor(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    culture_id: ObjectId
    name: str
    type: int

    class Config:
        arbitrary_types_allowed = True
