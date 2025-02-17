# Importamos FastAPI y Pydantic
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid

# Creamos la aplicación FastAPI
app = FastAPI(
    title="Sistema de Usuarios",
    description="API para gestión de usuarios",
    version="1.0.0"
)

# Lista en memoria para almacenar los usuarios (se puede reemplazar por una base de datos)
users = []

# Modelo de usuario usando Pydantic
class User(BaseModel):
    id: str
    name: str
    email: str
    username: str

# Endpoint para guardar un usuario (POST)
@app.post("/users/", tags=["Users"], status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    user.id = str(uuid.uuid4())  # Genera un UUID único para cada usuario
    users.append(user)
    return {"message": "Usuario agregado con éxito", "user": user}

# Endpoint para obtener todos los usuarios (GET)
@app.get("/users/", tags=["Users"], status_code=status.HTTP_200_OK)
def get_users():
    return {"users": users}