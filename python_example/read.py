from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
import time

# Creating engine

SQLALCHEMY_READ_DATABASE_URL = os.getenv("SQLALCHEMY_READ_DATABASE_URL", "postgresql://postgres:my_password@localhost:15002/postgres")

read_engine = create_engine(SQLALCHEMY_READ_DATABASE_URL)
PostgresReadSession = sessionmaker(autocommit=False, autoflush=False, bind=read_engine)

# ORM Model

Base = declarative_base()
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, Sequence("messages_id_seq"), primary_key=True)
    message = Column(String(150), nullable=False, unique=True)

    def __repr__(self):
        return "<Message(id='%s', message='%s')>" % (
            self.id,
            self.message,
        )

def get_messages(db):
    return db.query(Message).count()

if __name__ == "__main__":
    starttime = time.time()
    db = PostgresReadSession()
    while True:
        total_messages = get_messages(db)
        print(f"Result at [{time.time()}]: {total_messages}")
        time.sleep(1)