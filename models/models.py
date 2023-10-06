from sqlalchemy import create_engine, Column, Integer, String, URL, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()

db_url = URL.create(
    "mysql+mysqldb",
    username="root",
    password="MY$QL@l3x40!$!",
    host="localhost",
    database="ee_db",
)

engine = create_engine(db_url, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


class Collaborater(Base):
    __tablename__ = "collaboraters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String)
    team = Column(String)

    def __init__(self, id, username, email, password, phone, team):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.team = team

    def __repr__(self):
        return f"({self.id}) {self.username}, {self.email}, {self.phone}"


c1 = Collaborater(7, "TEST", "test@gmail.com", "Test1234", "0612233456", "support_team")

session.add(c1)
session.commit()
