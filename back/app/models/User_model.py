from sqlalchemy import create_engine, String, Column, Integer, DateTime, Text, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'USUARIOS'
    
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    NOMBRES = Column(String(100))
    APELLIDOS = Column(String(100))
    USERNAME = Column(String(50), unique=True, nullable=False)
    EMAIL = Column(String(100), unique=True, nullable=False)
    PASSWORD = Column(Text, nullable=False)
    TELEFONO = Column(String(20))
    DIRECCION = Column(Text)
    CIUDAD = Column(String(50))
    PAIS = Column(String(50))
    FECHA_NACIMIENTO = Column(Date)
    GENERO = Column(String(10))
    FOTO_PERFIL = Column(Text)
    FECHA_CREACION = Column(DateTime, default=datetime.utcnow)
    FECHA_ACTUALIZACION = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ULTIMO_LOGIN = Column(DateTime)
    ACTIVO = Column(Boolean, default=True)