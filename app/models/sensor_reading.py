from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class SensorReading(BaseModel):
  id: Optional[PydanticObjectId] = Field(alias="_id")
  sensor_id: ObjectId
  value: str
  date: datetime = datetime.utcnow()

  class Config:
    arbitrary_types_allowed = True
