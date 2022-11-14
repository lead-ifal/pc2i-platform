from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.models.objectid import PydanticObjectId
from bson import ObjectId

class User(BaseModel):
  id: Optional[PydanticObjectId] = Field(alias="_id")
  validation_date: Optional[str]
  encrypted_email: str
  validation: bool
  token: ObjectId
  email: str
  name: str
  password: bytes
  date_added: datetime = datetime.utcnow()

  class Config:
    arbitrary_types_allowed = True
