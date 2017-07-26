# log.py

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    def __init__(self, type, date):
        self.type = type
        self.date = date

metadata = Base.metadata

# end of file
