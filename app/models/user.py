from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId

class User(BaseModel):
  id: Optional[PydanticObjectId] = Field(alias="_id")
  token: str
  email: str
  name: str
  password: bytes
  date_added: datetime = datetime.utcnow()
