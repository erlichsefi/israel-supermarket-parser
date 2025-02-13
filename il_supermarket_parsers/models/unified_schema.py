from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union


class SchemaField(BaseModel):
    description: str
    length: Optional[Union[int, str]]
    type: Literal["numeric", "alphanumeric", "date", "time"]
    name: str
    include: bool = True


class StoreFileSchema(BaseModel):
    fields: List[SchemaField]
    version: str
    last_updated: str


class PriceFullFileSchema(BaseModel):
    fields: List[SchemaField]
    currency: str
    effective_date: str


class PromoFullFileSchema(BaseModel):
    fields: List[SchemaField]
    discount_type: str
    valid_until: str


class UniformSchema(BaseModel):
    store_file: StoreFileSchema
    price_full_file: PriceFullFileSchema
    promo_full_file: PromoFullFileSchema

    @classmethod
    def from_json_file(cls, json_path: str) -> "UniformSchema":
        """Load schema from JSON file"""
        import json

        with open(json_path, "r") as f:
            data = json.load(f)
            return cls(**data)
