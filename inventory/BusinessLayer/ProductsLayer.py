import time
from sqlalchemy.sql.elements import and_
from inventory.Models.ProductsModel import Products
from weavedin.settings import Session
from inventory.BusinessLayer import NotifyLayer
from inventory.MessageLayer import Message

session = Session()


def get_valid_products():
    try:
        return session.query(Products).filter(Products.is_valid).order_by(Products.name).all()
    except:
        Message.ErrorHandler(session)
        return False

def get_product_name(id):
    try:
        return session.query(Products.name).filter(Products.id == id).scalar()
    except:
        Message.ErrorHandler(session)
        return False

def is_unique_product_name(name):
    try:
        return len(session.query(Products).filter(Products.name == name).all()) <= 0
    except:
        Message.ErrorHandler(session)
        return False

def is_unique_product_code(code):
    try:
        return len(session.query(Products).filter(Products.code == code).all()) <= 0
    except:
        Message.ErrorHandler(session)
        return False

def is_unique_product_name_e(id, name):
    try:
        return len(session.query(Products).filter(and_(Products.id != id, Products.name == name)).all()) <= 0
    except:
        Message.ErrorHandler(session)
        return False

def is_unique_product_code_e(id, code):
    try:
        return len(session.query(Products).filter(and_(Products.id != id, Products.code == code)).all()) <= 0
    except:
        Message.ErrorHandler(session)
        return False

def insert_product(name, code, description, user_id):

    try:
        info = "Failure to update."
        status = False

        if not is_unique_product_name(name):
            info = "Product name must be unique"
        elif not is_unique_product_code(code):
            info = "Product code must be unique"
        else:

            date_stamp = time.strftime('%Y-%m-%d %H:%M:%S')

            product = Products(
                name=name,
                code=code,
                description=description,
                is_valid=1,
                user_id=user_id,
                date_stamp=date_stamp
            )

            session.add(product)
            session.commit()

            notifications = [9]

            #product.id is None until committed!
            NotifyLayer.insert_notification(notifications, product.id, user_id, date_stamp)

            session.commit()

            status = True
            info = "Success!!"

        return status, info

    except:
        Message.ErrorHandler(session)
        return False, "Error!"

def update_product(id, user_id, values, notifications, date_stamp):

    try:
        info = "Failure to update."
        status = False

        session.query(Products).filter(Products.id == id).update(values)

        NotifyLayer.insert_notification(notifications, id, user_id, date_stamp)

        session.commit()

        status = True
        info = "Success!!"

        return status, info

    except:
        Message.ErrorHandler(session)
        return False, "Error!"


def delete_product(id, user_id):

    try:
        info = "Failure to update."
        status = False
        date_stamp = time.strftime('%Y-%m-%d %H:%M:%S')

        values = {
            "is_valid": 0,
            "user_id": user_id,
            "date_stamp": date_stamp
        }

        session.query(Products).filter(Products.id == id).update(values)

        notifications = [10]
        NotifyLayer.insert_notification(notifications, id, user_id, date_stamp)

        session.commit()

        status = True
        info = "Success!!"

        return status, info

    except:
        Message.ErrorHandler(session)
        return False, "Error!"
