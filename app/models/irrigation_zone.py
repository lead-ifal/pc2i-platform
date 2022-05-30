from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class IrrigationZone(BaseModel):
  id: Optional[PydanticObjectId] = Field(alias="_id")
  user_id: str
  name: str
  description: str
  size: float
