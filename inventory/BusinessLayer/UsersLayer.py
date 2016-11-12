from inventory.Models.UsersModel import Users
from weavedin.settings import Session
from inventory.MessageLayer import Message

session = Session()


def get_valid_users():
    try:
        return session.query(Users).order_by(Users.username).all()

    except:
        Message.ErrorHandler(session)
        return None


def get_username(user_id):
    try:
        return session.query(Users.username).filter(Users.id == user_id).scalar()

    except:
        Message.ErrorHandler(session)
        return None
