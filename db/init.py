from db.base import Base
from db.session import engine
from db.models.task import Task

def init_db():
    Base.metadata.create_all(bind=engine)