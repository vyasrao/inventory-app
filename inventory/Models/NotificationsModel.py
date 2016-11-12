from sqlalchemy import Column, String, ForeignKey, event
from sqlalchemy.types import TIMESTAMP, BOOLEAN, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from inventory.Models import UsersModel
from weavedin import settings
from weavedin.settings import Session

session = Session()
Base = declarative_base()


class NotificationObject(Base):
    __tablename__ = 'notify_objects'

    id = Column(INTEGER, primary_key=True)
    object = Column(String(20))
    url = Column(String(100))

    def insert_initial_values(*args, **kwargs):

        session.add(NotificationObject(id=1, object="product", url="/inventory/product"))
        session.add(NotificationObject(id=2, object="variant", url="/inventory/variant"))
        session.commit()

        #NotificationType.insert_initial_values()


class NotificationType(Base):
    __tablename__ = 'notify_types'

    id = Column(INTEGER, primary_key=True)
    type = Column(String(20))
    object_id = Column(INTEGER, ForeignKey(NotificationObject.id))


    def insert_initial_values(*args, **kwargs):
        session.add(NotificationType(id=1, type="name", object_id=1))
        session.add(NotificationType(id=2, type="code", object_id=1))
        session.add(NotificationType(id=3, type="description", object_id=1))
        session.add(NotificationType(id=4, type="name", object_id=2))
        session.add(NotificationType(id=5, type="code", object_id=2))
        session.add(NotificationType(id=6, type="description", object_id=2))
        session.add(NotificationType(id=7, type="selling price", object_id=2))
        session.add(NotificationType(id=8, type="cost price", object_id=2))
        session.add(NotificationType(id=9, type="created", object_id=1))
        session.add(NotificationType(id=10, type="deleted", object_id=1))
        session.add(NotificationType(id=11, type="created", object_id=2))
        session.add(NotificationType(id=12, type="deleted", object_id=2))

        session.commit()


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(INTEGER, primary_key=True)
    type_id = Column(INTEGER, ForeignKey(NotificationType.id))
    view_user_id = Column(INTEGER, ForeignKey(UsersModel.Users.id))
    actor_user_id = Column(INTEGER, ForeignKey(UsersModel.Users.id))
    reference_id = Column(INTEGER)
    date_stamp = Column(TIMESTAMP)
    is_read = Column(BOOLEAN)
    is_valid = Column(BOOLEAN)


event.listen(NotificationObject.__table__, 'after_create', NotificationObject.insert_initial_values)
event.listen(NotificationType.__table__, 'after_create', NotificationType.insert_initial_values)

Base.metadata.create_all(settings.engine)
