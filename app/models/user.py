from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
  email: str
  name: str
  password: bytes
  date_added: datetime = datetime.utcnow()
