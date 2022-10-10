import os.path
from typing import Union
from typing import Optional
from fastapi import FastAPI, status
from pydantic import BaseModel
from src.database import Session
from src.models import ItemDB, OrderDB, OrdersDB
from src.database import Base, engine


app = FastAPI()
db = Session()

# Create the database if it doesn't exist
if not os.path.isfile('data.db'):
    Base.metadata.create_all(engine)


class Item(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    product_id: int
    quantity: int


class Orders(BaseModel):
    name: str
    address: str
    orders: list[Order]


@app.get("/items/{item_id}", tags=["items"], status_code=status.HTTP_200_OK)
def get_item(item_id: int):
    items = db.query(ItemDB).filter(ItemDB.id == item_id).first()

    if items is None:
        return {"message": "Item not found"}

    return items


@app.get("/items", tags=["items"], status_code=status.HTTP_200_OK)
def get_all_items():
    items = db.query(ItemDB).all()
    return items


@app.post("/item/", tags=["items"], status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    try:
        new_item = ItemDB(name=item.name, price=item.price)
        db.add(new_item)
        db.commit()
        return {"message": "Item created successfully"}

    except:
        return {"message": "An error occurred creating the item."}


@app.post("/order/", tags=["orders"], status_code=status.HTTP_201_CREATED)
def create_order(order: Orders):
    obj = db.query(OrdersDB).order_by(OrdersDB.id.desc()).first()
    if obj is None:
        order_id = 1
    else:
        order_id = obj.id + 1

    client_name = order.name
    client_address = order.address

    print(client_name)
    print(client_address)

    total_price = 0
    invoice = {"Purchased Items": [], "Total Price": 0}

    for item in order.orders:
        # check if the item exists
        item_obj = db.query(ItemDB).filter(
            ItemDB.id == item.product_id).first()
        if item_obj is None:
            return {"message": "Item not found"}

        new_order = OrderDB(product_id=item.product_id,
                            quantity=item.quantity)
        invoice["Purchased Items"].append(
            {"Item Name": item_obj.name, "Item Price": item_obj.price, "Quantity": item.quantity})
        total_price += item_obj.price * item.quantity
        db.add(new_order)
        db.commit()

        new_purchase = OrdersDB(
            id=order_id,
            name=client_name,
            address=client_address,
            order_id=new_order.id
        )

        db.add(new_purchase)
        db.commit()

    invoice["Total Price"] = total_price
    return invoice
