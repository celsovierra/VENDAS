from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    sku = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    cost_price = Column(Float, default=0)
    sale_price = Column(Float, default=0)
    stock = Column(Integer, default=0)
    temu_url = Column(String)
    temu_supplier = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    marketplace = Column(String)
    external_id = Column(String)
    status = Column(String, default="draft")
    product = relationship("Product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    marketplace = Column(String, index=True)
    external_id = Column(String, index=True)
    buyer_name = Column(String)
    status = Column(String)
    total = Column(Float, default=0)
    marketplace_fee = Column(Float, default=0)
    shipping_cost = Column(Float, default=0)
    product_cost = Column(Float, default=0)
    profit = Column(Float, default=0)
    temu_purchased = Column(Integer, default=0)
    temu_order_ref = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    title = Column(String)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, default=0)
    order = relationship("Order", back_populates="items")

class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String)
