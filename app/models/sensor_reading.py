from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class SensorReading(BaseModel):
  id: Optional[PydanticObjectId] = Field(alias="_id")
  sensor_id: str
  name: str
  value: str
  date: datetime = datetime.utcnow()
