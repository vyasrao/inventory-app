from itertools import groupby
import sqlalchemy
from sqlalchemy import insert
from sqlalchemy.sql.elements import and_
from inventory.Models.UsersModel import Users
from inventory.Models.NotificationsModel import Notification, NotificationObject, NotificationType
from inventory.Models.ProductsModel import Variants, Products
from inventory.MessageLayer import Message
from weavedin.settings import Session

session = Session()


def insert_notification(notifications, reference_id, user_id, date_stamp):

    try:
        for notify in notifications:

            q = session.query(
                sqlalchemy.sql.expression.bindparam("type_id", notify),
                Users.id,
                sqlalchemy.sql.expression.bindparam("actor_user_id", int(user_id)),
                sqlalchemy.sql.expression.bindparam("reference_id", int(reference_id)),
                sqlalchemy.sql.expression.bindparam("date_stamp", date_stamp),
                sqlalchemy.sql.expression.bindparam("is_read", 0),
                sqlalchemy.sql.expression.bindparam("is_valid", 1),
            ).filter(Users.id != user_id)

            session.execute(insert(Notification).from_select((
                Notification.type_id,
                Notification.view_user_id,
                Notification.actor_user_id,
                Notification.reference_id,
                Notification.date_stamp,
                Notification.is_read,
                Notification.is_valid
            ), q))
    except:
        Message.ErrorHandler(session)
        raise

# TODO: filter_by() could be used for keyword arguments, but faced some problem
def query_notification(all_notification, user_id):

    try:
        if all_notification:

            values = {"is_read": 1}

            session.query(Notification).filter(Notification.view_user_id == user_id).update(values)

            q_variant = session.query(Notification.id, Users.username, NotificationObject.object, NotificationType.type,
                                      Variants.name, Notification.date_stamp). \
                join(NotificationType). \
                join(NotificationObject). \
                join(Users, Users.id == Notification.actor_user_id). \
                join(Variants, Variants.id == Notification.reference_id). \
                filter(and_(Notification.view_user_id == user_id, NotificationObject.id == 2, Notification.is_valid == 1)). \
                limit(1000)

            q_product = session.query(Notification.id, Users.username, NotificationObject.object, NotificationType.type,
                                      Products.name, Notification.date_stamp). \
                join(NotificationType). \
                join(NotificationObject). \
                join(Users, Users.id == Notification.actor_user_id). \
                join(Products, Products.id == Notification.reference_id). \
                filter(and_(Notification.view_user_id == user_id, NotificationObject.id == 1, Notification.is_valid == 1)). \
                limit(1000)
        else:
            q_variant = session.query(Notification.id, Users.username, NotificationObject.object, NotificationType.type,
                                      Variants.name, Notification.date_stamp). \
                join(NotificationType). \
                join(NotificationObject). \
                join(Users, Users.id == Notification.actor_user_id). \
                join(Variants, Variants.id == Notification.reference_id). \
                filter(and_(Notification.view_user_id == user_id, NotificationObject.id == 2, Notification.is_read == 0)). \
                limit(10)

            q_product = session.query(Notification.id, Users.username, NotificationObject.object, NotificationType.type,
                                      Products.name, Notification.date_stamp). \
                join(NotificationType). \
                join(NotificationObject). \
                join(Users, Users.id == Notification.actor_user_id). \
                join(Products, Products.id == Notification.reference_id). \
                filter(and_(Notification.view_user_id == user_id, NotificationObject.id == 1, Notification.is_read == 0)). \
                limit(10)

        result = q_variant.union(q_product).all()

        return result
    except:
        Message.ErrorHandler(session)
        return None


def show_notification(user_id, all_notification):

    try:
        result = query_notification(all_notification, user_id)

        result_set = []
        for row in result:
            if row[3] == "created":
                names = row[4] + "0xxx1"
            elif row[3] == "deleted":
                names = row[4] + "0xxx2"
            else:
                names = row[4]

            result_set.append([row[1], row[2], row[3], names, row[5]])

        notification = []

        sorted_results = sorted(result_set[0:], key=lambda x: (x[4], x[0]), reverse=True)

        for k1, g1 in groupby(sorted_results, lambda x: x[0]):
            grouped_by_name = list(g1)
            v1, v2 = [], []

            for k2, g2 in groupby(grouped_by_name, lambda x: (x[1], x[3])):  # type, name
                v1.append(list(g2))

            for k2, g2 in groupby(grouped_by_name, lambda x: (x[1], x[2])):  # type, changed
                v2.append(list(g2))

            if len(v1) < len(v2):
                for entry in v1:
                    entries = [changed for user, ptype, changed, pname, date in entry]
                    action =""
                    of = ""
                    if "0xxx1" not in entry[0][3] and "0xxx2" not in entry[0][3]:
                        action = "changed"
                        of = "of"

                    text = "%s %s %s %s %s: %s" %(entry[0][0], action, ', '.join(entries), of, entry[0][1], entry[0][3])

                    text = text.replace("0xxx1", "")
                    text = text.replace("0xxx2", "")

                    notification.append(text)
            else:
                for entry in v2:
                    entries = [pname for user, ptype, changed, pname, date in entry]
                    if entry[0][2] == "created":
                        of = ""
                        action = ""
                    elif entry[0][2] == "deleted":
                        of = ""
                        action = ""
                    else:
                        action = "changed"
                        of = "of"

                    text = "%s %s %s %s %s: %s" %(entry[0][0], action, entry[0][2], of, entry[0][1], ', '.join(entries))

                    text = text.replace("0xxx1", "")
                    text = text.replace("0xxx2", "")

                    notification.append(text)

        return notification
    except:
        Message.ErrorHandler(session)
        raise
        return None


def clear_notification(user_id):

    try:
        values ={"is_read": 1, "is_valid": 0}

        session.query(Notification).filter(Notification.view_user_id == user_id).update(values)

        session.commit()

    except:
        Message.ErrorHandler(session)
        return None
