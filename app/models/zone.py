from pydantic import BaseModel

class Zone(BaseModel):
  name: str
  description: str
  size: float