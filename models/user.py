# FastAPI's jsonable_encoder handles converting various non-JSON types,
# such as datetime between JSON types and native Python types.
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from uuid import UUID, uuid4
from pprint import pprint


# Pydantic, and Python's built-in typing are used to define a schema
# that defines the structure and types of the different objects stored
# in the recipes collection, and managed by this API.
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

from .objectid import PydanticObjectId

class User(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    slug: str
    name: str
    email: str
    date_added: Optional[datetime]
    date_updated: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        dict_encoders = {str: lambda x: PydanticObjectId(x) if PydanticObjectId.is_valid(x) else x}
        json_encoders = {PydanticObjectId: str}


    @classmethod
    def from_mongo(cls, data: dict):
        """We must convert _id into "id". """
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))
    

    def to_json(self):
        return jsonable_encoder(self, by_alias=True, exclude_none=True)


    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data

