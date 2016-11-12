import time
from sqlalchemy.sql.elements import and_
from inventory.Models.ProductsModel import Variants
from weavedin.settings import Session
from inventory.BusinessLayer import NotifyLayer
from inventory.MessageLayer import Message

session = Session()


def get_valid_variants(product_id):
    try:
        return session.query(Variants).filter(and_(Variants.product_id == int(product_id), Variants.is_valid)).order_by(Variants.name).all()
    except:
        Message.ErrorHandler(session)
        return False

def is_unique_variant_name(product_id, name):
    try:
        return len(session.query(Variants).filter(and_(Variants.product_id == product_id, Variants.name == name)).all()) <= 0
    except:
        Message.ErrorHandler(session)
        return False


def is_unique_variant_code(product_id, code):
    try:
        return len(session.query(Variants).filter(and_(Variants.product_id == product_id, Variants.code == code)).all()) <= 0
    except:
        Message.ErrorHandler(session)
        return False


def is_unique_variant_name_e(product_id, variant_id, name):
    try:
        return len(
            session.query(Variants).filter(and_(Variants.product_id == product_id, Variants.id != variant_id, Variants.name == name)).all()) <= 0
    except:
        Message.ErrorHandler(session)
        return False


def is_unique_variant_code_e(product_id, variant_id, code):

    try:
        return len(session.query(Variants).
                   filter(and_(Variants.product_id == product_id, Variants.id != variant_id, Variants.code == code)).
                   all()) <= 0
    except:
        Message.ErrorHandler(session)
        return False


def insert_variant(product_id, name, code, description, user_id, sell_price, cost_price, options):

    try:
        info = "Failure to update."
        status = False

        if not is_unique_variant_name(product_id, name):
            info = "Variant name must be unique"
        elif not is_unique_variant_code(product_id, code):
            info = "Variant code must be unique"
        else:

            date_stamp = time.strftime('%Y-%m-%d %H:%M:%S')

            variant = Variants(
                product_id=product_id,
                name=name,
                code=code,
                description=description,
                selling_price=sell_price,
                cost_price=cost_price,
                is_valid=1,
                user_id=user_id,
                date_stamp=date_stamp,
                options=options
            )

            session.add(variant)
            session.commit()

            notifications = [11]
            NotifyLayer.insert_notification(notifications, variant.id, user_id, date_stamp)
            session.commit()

            status = True
            info = "Success!!"

        return status, info

    except:
        Message.ErrorHandler(session)
        return False, "Error!"


def update_variant(variant_id, user_id, values, notifications, date_stamp):

    try:
        info = "Failure to update."
        status = False

        session.query(Variants).\
            filter(and_(Variants.id == variant_id)).\
            update(values)

        NotifyLayer.insert_notification(notifications, variant_id, user_id, date_stamp)

        session.commit()

        status = True
        info = "Success!!"

        return status, info

    except:
        Message.ErrorHandler(session)
        return False, "Error!"


def delete_variant(variant_id, user_id):

    try:
        info = "Failure to update."
        status = False
        date_stamp = time.strftime('%Y-%m-%d %H:%M:%S')

        values = {
            "is_valid": 0,
            "user_id": user_id,
            "date_stamp": date_stamp
        }

        session.query(Variants).filter(and_(Variants.id == variant_id)).update(values)

        notifications = [12]
        NotifyLayer.insert_notification(notifications, variant_id, user_id, date_stamp)

        session.commit()

        status = True
        info = "Success!!"

        return status, info

    except:
        Message.ErrorHandler(session)
        return False, "Error!"
