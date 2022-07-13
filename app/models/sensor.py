from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class Sensor(BaseModel):
  id: Optional[PydanticObjectId] = Field(alias="_id")
  culture_id: str
  name: str
  type: int
