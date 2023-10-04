from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


user = "root"
password = "MY$QL@l3x40!$!"
host = "localhost"
database = "ee_db"

mysql_url = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"

engine = create_engine(mysql_url)


Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Collaborater(Base):
    __tablename__ = "collaboraters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String)

    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="collaboraters")


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    team_name = Column(String, unique=True)

    collaboraters = relationship("Collaborater", back_populates="team")


class SalesTeam(Base):
    __tablename__ = "sales_team"
    id = Column(Integer, primary_key=True)


class GestureTeam(Base):
    __tablename__ = "gesture_team"
    id = Column(Integer, primary_key=True)


class SupportTeam(Base):
    __tablename__ = "support_team"
    id = Column(Integer, primary_key=True)
