from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from sensorrunner.secrets import POSTGRES

engine = create_engine(POSTGRES)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()


class SWITCHLOW(Base):
    __tablename__ = "SWITCHLOW"
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
            session.rollback()
            print(f"row {self.name} not added: {e}, rollback issued")

    def __repr__(self):
        return f"<SWITCHLOW(id='{self.id}', name={self.name}, created='{self.created_at}', duration={self.stop-self.start}), unit={self.unit}>"


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


class BMP390_ENTRY(Base):
    __tablename__ = "BMP390_ENTRY"
    __table_args__ = {"extend_existing": True}

    # TODO: SENSOR ID
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    #
    name = Column(String)
    temp_value = Column(Float)
    temp_unit = Column(String)
    pressure_value = Column(Float)
    pressure_unit = Column(String)
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
            f", rh='{self.pressure_value} {self.pressure_unit}', measurement_time={self.measurement_time})>"
        )


class PT19(Base):
    __tablename__ = "PT19"
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
            f"<PT19(id='{self.id}', name={self.name}, value='{self.value}', "
            f"unit={self.unit}, measurement_time={self.measurement_time})>"
        )


class VEML6070(Base):
    __tablename__ = "VEML6070"
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
            f"<VEML6070(id='{self.id}', name={self.name}, value='{self.value}', "
            f"unit={self.unit}, measurement_time={self.measurement_time})>"
        )


class CurrentDevice(Base):
    __tablename__ = "CurrentDevice"
    __table_args__ = {"extend_existing": True}

    # TODO: SENSOR ID

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    name = Column(String)
    disk_total_GB = Column(Float)
    disk_used_GB = Column(Float)
    mem_total_GB = Column(Float)
    mem_used_GB = Column(Float)
    load_min_avg = Column(Float)
    cpu_temp = Column(Float)
    num_pids = Column(Integer)
    wifi_isup = Column(Boolean)
    run_time_hrs = Column(Float)
    uuid_ident = Column(String)
    load_min_avg = Column(Float)
    load_min_avg = Column(Float)
    load_min_avg = Column(Float)
    mac = Column(String)
    measurement_time = Column(TIMESTAMP)

    def add(self, session):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            print(f"row {self.name} not added: {e}")

    def __repr__(self):
        return f"<CurrentDevice(id='{self.id}', name={self.name})>"


class VIB801S_Row(Base):
    __tablename__ = "VIB801S"
    __table_args__ = {"extend_existing": True}

    # TODO: SENSOR ID

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    #
    name = Column(String)
    state = Column(String)
    measurement_time = Column(TIMESTAMP)

    def add(self, session):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            print(f"row {self.name} not added: {e}")

    def __repr__(self):
        return f"<VIB801S(id='{self.id}', name={self.name},measurement_time={self.measurement_time})>"


class PM25_ENTRY(Base):
    __tablename__ = "PM25_ENTRY"
    __table_args__ = {"extend_existing": True}

    # TODO: SENSOR ID

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    #
    name = Column(String)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    num_iterations = Column(Integer)
    particle_03um = Column(Float)
    particle_05um = Column(Float)
    particle_10um = Column(Float)
    particle_25um = Column(Float)
    particle_50um = Column(Float)
    particle_100um = Column(Float)
    standard_pm10 = Column(Float)
    env_pm10 = Column(Float)
    standard_pm25 = Column(Float)
    env_pm25 = Column(Float)
    standard_pm100 = Column(Float)
    env_pm100 = Column(Float)
    particle_num_unit = Column(String)  # 100um/0.1L
    particle_concentration_unit = Column(String)  # ug/m^3

    def add(self, session):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            print(f"row {self.name} not added: {e}")

    def __repr__(self):
        return f"<PM25_ENTRY(id='{self.id}', name={self.name}, start_time={self.start_time})>"


class ESPCAM_Row(Base):
    __tablename__ = "cam"
    __table_args__ = {"extend_existing": True}

    # TODO: SENSOR ID

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    #
    name = Column(String)
    bucket = Column(String)
    index = Column(String)
    capture_time = Column(String)
    post_capture_time = Column(TIMESTAMP)
    file_path = Column(String)
    ip = Column(String)
    # TOOD: meta -- quality +

    def add(self, session):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            print(f"row {self.name} not added: {e}")

    def __repr__(self):
        return f"<CAM_Row(id='{self.id}', capture_time={self.capture_time}, bucket={self.bucket}, index={self.index}, file_path={self.file_path})>"


class PH_ENTRY(Base):
    __tablename__ = "ph"
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
            f"<PH_ENTRY(id='{self.id}', name={self.name}, value='{self.value}', "
            f"unit={self.unit}, measurement_time={self.measurement_time})>"
        )


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

# TODO: I'm not sure how to best handle this yet. We need multiple sessions, for
# concurrent interaction but I'm not sure global is best
SESSION_SWITCHLOW = Session()
SESSION_VL53l0X = Session()
SESSION_SI7021 = Session()
SESSION_PT19 = Session()
SESSION_VEML6070 = Session()
SESSION_CurrentDevice = Session()
SESSION_VIB801S = Session()
SESSION_PM25_ENTRY = Session()
SESSION_BMP390_ENTRY = Session()
SESSION_ESPCAM = Session()
SESSION_PH_ENTRY = Session()