from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class SensorType(BaseModel):
  id: Optional[PydanticObjectId] = Field(alias="_id")
  type : str
