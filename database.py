# pip install sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import database_exists

Base = declarative_base()

class Database(object):
    def __init__(self, db):
        
        self.engine = create_engine("sqlite:///{}".format(db))
        if database_exists(self.engine.url):
            Base.metadata.bind = self.engine
        else:
            Base.metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine, autoflush=False)

        self.session = DBSession()

#%%
# Item 
class Pool(Base):
    __tablename__ = "pool" 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    borough = Column(String)
    location = Column(String)
    pooltype = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    
    attendances = relationship("Attendance", back_populates="pool")

# Listing 
class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    
    pool_id = Column(Integer, ForeignKey("pool.id"))
    pool = relationship("Pool", back_populates="attendances")

    datetime = Column(DateTime)
    number = Column(Integer)
    air_temperature = Column(Float)
