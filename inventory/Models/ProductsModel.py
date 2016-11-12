from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.types import DECIMAL, TIMESTAMP, BOOLEAN, JSON, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from weavedin import settings
from inventory.Models import UsersModel

Base = declarative_base()


class Products(Base):
    __tablename__ = 'products'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(20))
    description = Column(String(100))
    code = Column(String(10))
    is_valid = Column(BOOLEAN)
    user_id = Column(INTEGER, ForeignKey(UsersModel.Users.id))
    date_stamp = Column(TIMESTAMP)


class Variants(Base):
    __tablename__ = 'variants'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(20))
    code = Column(String(20))
    description = Column(String(100))
    product_id = Column(INTEGER, ForeignKey(Products.id))
    selling_price = Column(DECIMAL)
    cost_price = Column(DECIMAL)
    options = Column(JSON)
    is_valid = Column(BOOLEAN)
    user_id = Column(INTEGER, ForeignKey(UsersModel.Users.id))
    date_stamp = Column(TIMESTAMP)


Base.metadata.create_all(settings.engine)
