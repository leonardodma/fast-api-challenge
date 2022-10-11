from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    product_id: int
    quantity: int


class Purchase(BaseModel):
    name: str
    address: str
    orders: list[Order]
