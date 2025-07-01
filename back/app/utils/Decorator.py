import jwt
from datetime import datetime, timedelta
import os
from fastapi import HTTPException, Request
import jsonschema
from jsonschema import validate
import json


class Response:
    """Clase para generar respuestas de manera estándar, 
        con su codigo de respuesta y mensaje de error"""
    
    """Class to generate standard responses,
    with their response code and error message"""

    @staticmethod
    def generate_response(function_name, status_code, data, error=False, custom_message=None):
        messages = {
            "register_user": "Usuario creado con éxito",
            "login_users": {
                200: "Sesión creada con éxito",
                400: "Usuario o contraseña incorrectos",
                404: "Usuario no encontrado"
            },
        }

        if function_name == "login_users" and status_code in messages["login_users"]:
            message = messages["login_users"][status_code]
        else:
            message = messages.get(function_name, custom_message if custom_message else "Operación exitosa")

        if error:
            response = {
                "service": function_name + "_service",
                "status_code": status_code,
                "error": True,
                "data": {
                    "message": message
                }
            }
        else:
            response = {
                "service": function_name + "service",
                "status_code": status_code,
                "error": False,
                "data": {
                    "message": message,
                    "data": data
                }
            }

        return response
    

    """Método para crear un token JWT"""
    """Method to create a JWT token"""

    def create_jwt_token(self, user_id, username, first_name, last_name, email):
        secret_key = os.getenv("SECRET_KEY")
        algorithm = os.getenv("ALGORITHM")
        
        expiration = datetime.utcnow() + timedelta(hours=1)

        exp_timestamp = expiration.timestamp()

        payload = {
            "id": user_id,
            "sub": username,
            "exp": exp_timestamp,
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }

        token = jwt.encode(payload, secret_key, algorithm=algorithm)
        return token
    
    """Método para validar un token JWT"""
    """Method to validate a JWT token"""

    def validate_jwt_token(token: str):
        try:
            secret_key = os.getenv("SECRET_KEY")
            algorithm = os.getenv("ALGORITHM")

            decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm])

            exp_timestamp = decoded_token["exp"]
            current_timestamp = datetime.utcnow().timestamp()

            exp_timestamp = int(exp_timestamp)
     
            if exp_timestamp < current_timestamp:
                raise Exception("Token expired")
            
            return decoded_token
        except jwt.ExpiredSignatureError:
                raise Exception("Token expired")
        except jwt.InvalidTokenError as e:
            print("La excepción es", e)
        raise Exception("Token expired")
    