from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default='user')


class Complain(Base):
    __tablename__ = "complains"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    complainRating = Column(Integer, nullable=False)
    timeLogged = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('NOW()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                      nullable=False)
    resolved = Column(String)
    owner = relationship("User")
