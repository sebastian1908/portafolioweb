from app.db.Database import Database
from app.models.User_model import UserModel
from fastapi.responses import JSONResponse
from argon2 import PasswordHasher
from app.utils.Decorator import Response as r
import re, inspect


class Users:

    """Clase para manejar usuarios registro y sessiones"""
    """Class for handling users registration and sessions"""

    def __init__(self):
        self.conn = Database()
        self.db = self.conn.setConnection()
        self.ph = PasswordHasher()

    """Método para realizar el registro de usuarios"""
    """Method for performing user registration"""

    def register_user(self, data):
        function_name = inspect.currentframe().f_code.co_name
        firstname = data["NOMBRES"]    
        last_name = data["APELLIDOS"]   
        username = data["USERNAME"]    
        email = data["EMAIL"]        
        password = data["PASSWORD"]
        phone = data["TELEFONO"]
        address = data["DIRECCION"]
        city = data["CIUDAD"]
        country = data["PAIS"]
        birthdate = data["FECHA_NACIMIENTO"]
        gender = data["GENERO"]
        photo = data["FOTO_PERFIL"]
        
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise Exception("Error, correo electrónico no tiene un formato válido")

        email_expr = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        validateEmail = self.db.query(UserModel).filter(UserModel.EMAIL == email).first()
        validateUser = self.db.query(UserModel).filter(UserModel.USERNAME == username).first()

        if not re.match(email_expr, email):
            raise Exception("Error, correo electrónico no tiene un formato válido")
        elif validateEmail:
            raise Exception("Error, el email esta en uso")
        elif validateUser:
            raise Exception("Error, el usuario esta en uso")
        else:
            pass

        hashed_password = self.ph.hash(password)

        new_user = UserModel(
            NOMBRES=firstname,
            APELLIDOS=last_name,
            USERNAME=username,
            EMAIL=email,
            PASSWORD=hashed_password,
            TELEFONO=phone,
            DIRECCION=address,
            CIUDAD=city,
            PAIS=country,
            FECHA_NACIMIENTO=birthdate,
            GENERO=gender,
            FOTO_PERFIL=photo
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        if new_user.ID:
            response = r.generate_response(function_name, 201, new_user.ID)
        else:
            response = r.generate_response(function_name, 400, None, error=True, custom_message="Error al crear usuario")

        return JSONResponse(content=response, status_code=201)
    
    """Método para realizar el login de usuarios"""
    """Method for performing user login"""

    def login_users(self, data):
        function_name = inspect.currentframe().f_code.co_name
        usuario = data["USERNAME"]
        passw = data["PASSWORD"]

        query = self.db.query(UserModel).filter(UserModel.USERNAME == usuario).first()

        if query:
            try:
                self.ph.verify(query.PASSWORD, passw)
                access_token = r.create_jwt_token(self, query.ID, query.USERNAME, query.APELLIDOS, query.NOMBRES, query.EMAIL)
                response = r.generate_response(function_name, 200, access_token)
                json_response = JSONResponse(content=response, status_code=200)
             
                return json_response
            except Exception as e:
                response = r.generate_response(function_name, 400, None, error=True, custom_message="Contraseña incorrecta")
                return JSONResponse(content=response, status_code=400)
        else:
            response = r.generate_response(function_name, 404, None, error=True, custom_message="Usuario no encontrado")
            return JSONResponse(content=response, status_code=404)
