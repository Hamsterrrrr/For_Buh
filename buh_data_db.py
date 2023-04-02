from sqlalchemy import create_engine
from sqlalchemy import String, Integer, Column, Table, MetaData, UniqueConstraint, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



engine = create_engine("postgresql+psycopg2://postgres:b,hf20043004@localhost/database")
Base = declarative_base()


# class Users(Base):
#     __tablename__ = "Users"
#     ID = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     inns = relationship("Inns", back_populates="User")

class Inns(Base):
    __tablename__ = "Inns"
    ID = Column(Integer, primary_key=True)
    inn = Column(String, unique=True)
    # user_id = Column(Integer, ForeignKey("Users.ID"))
    # user = relationship("Users", back_populates="inns")
    codes_data = relationship("Codes_data", backref="inn")
    formes_data = relationship("Formes_data", backref="inn")

class Codes_data(Base):
    __tablename__ = "Codes_data"
    ID = Column(Integer, primary_key=True)
    OKPO = Column(String)
    OGRN = Column(String)
    DATA_registration = Column(String)
    INN = Column(String)
    OKATO_faction = Column(String)
    OKATO_registration = Column(String)
    OKTMO_faction = Column(String)
    OKTMO_registration = Column(String)
    OKOGU = Column(String)
    OKFS = Column(String)
    inn_id = Column(Integer, ForeignKey("Inns.ID"))
    UniqueConstraint(INN, name="uix_1")

class Formes_data(Base):
    __tablename__="Formes_data"
    ID = Column(Integer, primary_key=True)
    Index = Column(String)
    Names_formes = Column(String)
    Periodes_formes = Column(String)
    Deadline = Column(String)
    Reporting_period = Column(String)
    Comments = Column(String)
    OKUD = Column(String)
    inn_id = Column(Integer, ForeignKey("Inns.ID"))


if __name__=="__main__":
    Base.metadata.create_all(engine)