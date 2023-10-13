from sqlalchemy import (
    create_engine,
    URL,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Uuid,
    Date,
    Float,
)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from decouple import config


Base = declarative_base()


class Event(Base):
    """
    Create Events table
    """

    __tablename__ = "event"

    id = Column("id", Uuid, primary_key=True, unique=True)
    contract_id = Column("contract_id", Uuid, ForeignKey("contract.id"))
    contract = relationship("Contract")
    customer_name = Column("customer_name", String, ForeignKey("customer.name"))
    customer = relationship("Customer")
    start_date = Column("start_date", Date)
    end_date = Column("end_date", Date)
    support_username = Column("support_username", ForeignKey("collaborater.username"))
    support = relationship("Collaborater")
    location = Column("location", String)
    attendees = Column("attendees", Integer)
    description = Column("description", String)

    def __repr__(self):
        return f"Event {self.id}"


class Contract(Base):
    """
    Create Contracts table
    """

    __tablename__ = "contract"

    id = Column("id", Uuid, primary_key=True, unique=True)
    customer_name = Column("customer_name", String, ForeignKey("customer.name"))
    customer = relationship("Customer")
    commercial_username = Column(
        "commercial_username", String, ForeignKey("collaborater.username")
    )
    commercial = relationship("Collaborater")
    price = Column("price", Float)
    create_date = Column("create_date", Date)
    status = Column("status", Boolean, default=False)
    events = relationship(Event, backref="events_contract")

    def __repr__(self):
        return f"Contract {self.id}"


class Customer(Base):
    """
    Create Customers table
    """

    __tablename__ = "customer"

    id = Column("id", Uuid, primary_key=True, unique=True)
    name = Column("name", String, unique=True)
    email = Column("email", String, unique=True)
    phone = Column("phone", Integer, unique=True)
    company = Column("company", String)
    create_date = Column("create_date", Date)
    update_date = Column("update_date", Date)
    commercial_username = Column(
        "commercial_username", String, ForeignKey("collaborater.username")
    )
    commercial = relationship("Collaborater")
    contracts = relationship(Contract, backref="contracts_customer")
    events = relationship(Event, backref="events_customer")

    def __repr__(self):
        return f"Customer {self.name}"


class Collaborater(Base):
    """
    Create Collaboraters table
    """

    __tablename__ = "collaborater"

    id = Column("id", Uuid, primary_key=True, unique=True)
    phone = Column("phone", Integer, unique=True)
    email = Column("email", String, unique=True)
    username = Column("username", String, unique=True)
    password = Column("password", String)
    role = Column("role", String)
    customers = relationship(Customer, backref="customers_collaborater")
    contracts = relationship(Contract, backref="contracts_collaborater")
    events = relationship(Event, backref="events_collaborater")

    def __repr__(self):
        return f"User {self.username}"


def init_base():
    USERNAME = config("DB_USER")
    PASSWORD = config("DB_PASSWORD")
    HOST = config("DB_HOST")
    DATABASE = config("DB_NAME")

    db_url = URL.create(
        "postgresql+psycopg2",
        username=f"{USERNAME}",
        password=f"{PASSWORD}",
        host=f"{HOST}",
        database=f"{DATABASE}",
    )

    engine = create_engine(db_url, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    return engine, session
