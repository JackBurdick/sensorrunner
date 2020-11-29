from sqlalchemy import Column, Integer, String, TIMESTAMP, Float
from datetime import timedelta, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from aeropi.secrets import POSTGRES

engine = create_engine(POSTGRES)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()


class MyRow(Base):
    __tablename__ = "things"
    __table_args__ = {"extend_existing": True}

    # TODO: SENSOR ID
    # TODO: PINS

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    #
    name = Column(String)
    start = Column(TIMESTAMP)
    stop = Column(TIMESTAMP)
    unit = Column(String)

    def add(self, session):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            print(f"row {self.name} not added: {e}")

    def __repr__(self):
        return f"<MyRow(id='{self.id}', name={self.name}, created='{self.created_at}', duration={self.stop-self.start}), unit={self.unit}>"


class VL53l0X(Base):
    __tablename__ = "VL53l0X"
    __table_args__ = {"extend_existing": True}

    # TODO: SENSOR ID

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    #
    name = Column(String)
    value = Column(Float)
    unit = Column(String)
    measurement_time = Column(TIMESTAMP)

    def add(self, session):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            print(f"row {self.name} not added: {e}")

    def __repr__(self):
        return (
            f"<VL53l0X(id='{self.id}', name={self.name}, value='{self.value}', "
            f"unit={self.unit}, measurement_time={self.measurement_time})>"
        )


class SI7021(Base):
    __tablename__ = "SI7021"
    __table_args__ = {"extend_existing": True}

    # TODO: SENSOR ID

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    #
    name = Column(String)
    temp_value = Column(Float)
    temp_unit = Column(String)
    rh_value = Column(Float)
    rh_unit = Column(String)
    measurement_time = Column(TIMESTAMP)

    def add(self, session):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            print(f"row {self.name} not added: {e}")

    def __repr__(self):
        return (
            f"<SI7021(id='{self.id}', name={self.name}, temp='{self.temp_value} *{self.temp_unit}'"
            f", rh='{self.rh_value} {self.rh_unit}', measurement_time={self.measurement_time})>"
        )


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

# TODO: I'm not sure how to best handle this yet. We need multiple sessions, for
# concurrent interaction but I'm not sure global is best
SESSION_MyRow = Session()
SESSION_VL53l0X = Session()
SESSION_SI7021 = Session()
