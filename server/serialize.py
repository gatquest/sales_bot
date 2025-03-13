from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional

class Order(BaseModel):
    id: int
    client: str
    photo: str
    country: int
    size: str
    price: float


class CreateOrder(BaseModel):
    client_name: str
    to_russia: str
    size: str
    price: float
    order_type: Optional[str] = None

    # @field_validator('size')
    # def validate_size(cls, value):
    #     if value not in ['small', 'medium', 'large']:
    #         raise ValueError('Size must be one of: small, medium, large')
    #     return value

    # @field_validator('price')
    # def validate_price(cls, value):
    #     if value <= 0:
    #         raise ValueError('Price must be greater than 0')
    #     return value


class UpdateOrder(BaseModel):
    client: str
    photo: str
    country: int
    size: str
    price: float


class GetOrder(BaseModel):
    order_number: int



class ReplyGetOrder(BaseModel):
    id: int
    order_number: int
    client_name: str
    order_date: str
    image_path: str