from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
import time


# Creating engine

SQLALCHEMY_WRITE_DATABASE_URL = os.getenv("SQLALCHEMY_WRITE_DATABASE_URL", "postgresql://postgres:my_password@localhost:15001/postgres")

write_engine = create_engine(SQLALCHEMY_WRITE_DATABASE_URL)
PostgresWriteSession = sessionmaker(autocommit=False, autoflush=False, bind=write_engine)

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

def create_message(db, message):
    entity = Message(message=message)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


Base.metadata.create_all(write_engine)

if __name__ == "__main__":
    starttime = time.time()
    db = PostgresWriteSession()
    while True:
        created_message = create_message(db, f"Message created at {time.time()}")
        print(f"Created message: {created_message}")
        time.sleep(1)