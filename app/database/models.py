from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class ItemDB(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    price = Column(Float(precision=2), nullable=False)

    def __repr__(self):
        return f"Item(name='{self.name}', price={self.price})"


class OrderDB(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Order(product_id={self.product_id}, quatity={self.quantity})"


class PurchaseDB(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(80), nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)

    def __repr__(self):
        return f"Purchase(name='{self.name}', address={self.address}, order_id={self.order_id})"
