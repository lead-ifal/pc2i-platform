from pydantic import BaseModel, Field

class Zone(BaseModel):
  id: int = Field(alias="_id")
  name: str
  description: str
  size: float
