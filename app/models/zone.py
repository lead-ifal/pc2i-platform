from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class Zone(BaseModel):
  id: Optional[PydanticObjectId] = Field(alias="_id")
  user_id: str
  name: str
  description: str
  size: float
