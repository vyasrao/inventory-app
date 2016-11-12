from sqlalchemy import Column, String, event
from sqlalchemy.types import BOOLEAN, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from weavedin import settings
from weavedin.settings import Session

session = Session()

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True)
    username = Column(String(20))
    is_valid = Column(BOOLEAN)

    def insert_initial_values(*args, **kwargs):

        session.add(Users(id=1, username="vyas", is_valid=1))
        session.add(Users(id=2, username="jose", is_valid=1))
        session.add(Users(id=3, username="rao", is_valid=1))
        session.commit()


event.listen(Users.__table__, 'after_create', Users.insert_initial_values)

Base.metadata.create_all(settings.engine)
