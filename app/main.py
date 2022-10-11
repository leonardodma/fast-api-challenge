import os.path
from fastapi import status
from app import app, Item, Order, Purchase
from app.database import db, ItemDB, OrderDB, PurchaseDB
from app.utils import remove_from_db
from propreties import SQLITE_DATA_PATH


@app.get("/items/{item_id}", tags=["Items"], status_code=status.HTTP_200_OK)
async def get_item(item_id: int):
    items = db.query(ItemDB).filter(ItemDB.id == item_id).first()

    if items is None:
        return {"message": "Item not found"}

    return items


@app.get("/items", tags=["Items"], status_code=status.HTTP_200_OK)
async def get_all_items():
    items = db.query(ItemDB).all()
    return items


@app.post("/item/", tags=["Items"], status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    try:
        new_item = ItemDB(name=item.name, price=item.price)
        db.add(new_item)
        db.commit()
        return {"message": "Item created successfully"}

    except:
        return status.HTTP_422_UNPROCESSABLE_ENTITY


@app.post("/purchase/", tags=["Purchase"], status_code=status.HTTP_201_CREATED)
async def create_purchase(purchase: Purchase):
    # get the purchase id
    obj = db.query(PurchaseDB).order_by(PurchaseDB.id.desc()).first()
    if obj is None:
        purchase_id = 1
    else:
        purchase_id = obj.id + 1

    # get name and address
    try:
        client_name = purchase.name
        client_address = purchase.address
    except:
        return status.HTTP_422_UNPROCESSABLE_ENTITY

    # Process the order
    total_price = 0
    invoice = {"Purchased Items": [], "Total Price": 0}

    # List to stores order and purchases
    order_list = []
    purchase_list = []

    for item in purchase.orders:
        # check if the item exists
        item_obj = db.query(ItemDB).filter(
            ItemDB.id == item.product_id).first()
        if item_obj is None:
            # Remove the order from the database
            remove_from_db(order_list, purchase_list)
            return {"message": f"Item with id {item.product_id} were not found"}

        # check if the order is valid
        try:
            new_order = OrderDB(product_id=item.product_id,
                                quantity=item.quantity)
        except:
            # Remove the order from the database
            remove_from_db(order_list, purchase_list)
            return status.HTTP_422_UNPROCESSABLE_ENTITY

        # Put the order in the invoice
        invoice["Purchased Items"].append(
            {"name": item_obj.name, "price": item_obj.price, "quantity": item.quantity})
        total_price += item_obj.price * item.quantity

        # Add the order to the order list
        db.add(new_order)
        db.commit()
        order_list.append(new_order.id)

        # add the purchase to the list
        new_purchase = PurchaseDB(
            id=purchase_id,
            name=client_name,
            address=client_address,
            order_id=new_order.id
        )

        db.add(new_purchase)
        db.commit()
        purchase_list.append(purchase_id)

    invoice["Total Price"] = total_price

    return invoice
