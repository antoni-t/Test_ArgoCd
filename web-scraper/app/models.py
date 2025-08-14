import os
import time
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, TIMESTAMP, UniqueConstraint, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

Base = declarative_base()

class GenerationTable(Base):
    """
    SQLAlchemy model for the powergeneration table.
    """
    __tablename__ = 'generation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wattage = Column(Float(precision=2), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)  # UTC timestamp
    power_type = Column(Integer, primary_key=True, nullable=False)
    region = Column(String(15), primary_key=True, nullable=False)
    __table_args__ = (UniqueConstraint('timestamp', 'power_type',
                      'region', name='_timestamp_power_type_region_uc'),)

class ConsumptionTable(Base):
    """
    SQLAlchemy model for the powerconsumption table.
    """
    __tablename__ = 'consumption'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wattage = Column(Float(precision=2), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)  # UTC timestamp
    power_type = Column(Integer, primary_key=True, nullable=False)
    region = Column(String(15), primary_key=True, nullable=False)
    __table_args__ = (UniqueConstraint('timestamp', 'power_type',
                      'region', name='_timestamp_power_type_region_uc'),)

class PowerTypeMappingTable(Base):
    """
    SQLAlchemy model for the powertypemapping table.
    """
    __tablename__ = 'powertypemapping'
    power_type_id = Column(Integer, primary_key=True, nullable=False)
    power_type_name = Column(String(255), nullable=False)

# Database connection
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')  # Default port for MySQL
DB_NAME = os.getenv('DB_NAME', 'powerdata')

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
databaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def wait_for_db():
    """
    Wait until the database is available.
    """
    while True:
        try:
            engine.connect()
            print("Database is available.")
            break
        except OperationalError:
            print("Database is not available yet. Retrying in 5 seconds...")
            time.sleep(5)

def create_tables_if_not_exist():
    """
    Create tables if they do not exist in the database.

    This function uses SQLAlchemy's inspect module to check if the tables
    'powergeneration', 'powerconsumption', and 'powertypemapping' exist.
    If they do not exist, it creates them.
    """
    inspector = inspect(engine)
    if not inspector.has_table(GenerationTable.__tablename__):
        GenerationTable.__table__.create(bind=engine)
    if not inspector.has_table(ConsumptionTable.__tablename__):
        ConsumptionTable.__table__.create(bind=engine)
    if not inspector.has_table(PowerTypeMappingTable.__tablename__):
        PowerTypeMappingTable.__table__.create(bind=engine)

def populate_power_type_mapping():
    """
    Populate the PowerTypeMapping table with default power types if they do not exist.

    This function checks if the PowerTypeMapping table is populated with the default
    power types. If not, it inserts the missing entries.
    """
    default_power_types = {
        1223: 'Stromerzeugung: Braunkohle',
        1224: 'Stromerzeugung: Kernenergie',
        1225: 'Stromerzeugung: Wind Offshore',
        1226: 'Stromerzeugung: Wasserkraft',
        1227: 'Stromerzeugung: Sonstige Konventionelle',
        1228: 'Stromerzeugung: Sonstige Erneuerbare',
        4066: 'Stromerzeugung: Biomasse',
        4067: 'Stromerzeugung: Wind Onshore',
        4068: 'Stromerzeugung: Photovoltaik',
        4069: 'Stromerzeugung: Steinkohle',
        4070: 'Stromerzeugung: Pumpspeicher',
        4071: 'Stromerzeugung: Erdgas',
        410: 'Stromverbrauch: Gesamt (Netzlast)',
        4359: 'Stromverbrauch: Residuallast',
        4387: 'Stromverbrauch: Pumpspeicher'
    }

    session = databaseSession()
    try:
        for power_type_id, power_type_name in default_power_types.items():
            existing_entry = session.query(PowerTypeMappingTable).filter_by(
                power_type_id=power_type_id).first()
            if not existing_entry:
                new_entry = PowerTypeMappingTable(
                    power_type_id=power_type_id, power_type_name=power_type_name)
                session.add(new_entry)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"{datetime.now()}: Error: {e}")
    finally:
        session.close()