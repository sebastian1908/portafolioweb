import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv() 

class Database:

    def __init__(self):
        self.user = os.getenv("BD_USER")
        self.password = os.getenv("BD_PASSWORD")
        self.port = os.getenv("DB_PORT")
        self.server = os.getenv("DB_HOST")
        self.database = os.getenv("BD_NAME")

        if not all([self.user, self.password, self.port, self.server, self.database]):
            raise ValueError("Faltan variables de entorno requeridas para la conexión a la base de datos.")

        self.engine = self.getconnection()

    def getconnection(self):
        user = quote_plus(self.user)
        password = quote_plus(self.password)
        host = self.server
        port = self.port
        db = self.database
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

        return create_engine(connection_string)

    def setConnection(self):
        session = sessionmaker(bind=self.engine)
        return session()
