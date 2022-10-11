from app.database import db, ItemDB, OrderDB, PurchaseDB

def remove_from_db(order_list, purchase_list):
    # Remove the order from the database
    for id in order_list:
        db.query(OrderDB).filter(OrderDB.id == id).delete()

    # Remove the purchases from the database
    for id in purchase_list:
        db.query(PurchaseDB).filter(PurchaseDB.id == id).delete()

    db.commit()