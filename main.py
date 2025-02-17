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

# Lista en memoria para almacenar los usuarios (puede ser reemplazada por una base de datos)
users = []

# Modelo de usuario usando Pydantic
class User(BaseModel):
    name: str
    email: str
    username: str

# Endpoint para guardar un usuario (POST)
@app.post("/users/", tags=["Users"], status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    new_user = {"id": str(uuid.uuid4()), **user.dict()}
    users.append(new_user)
    return {"message": "Usuario agregado con éxito", "user": new_user}

# Endpoint para obtener todos los usuarios (GET)
@app.get("/users/", tags=["Users"], status_code=status.HTTP_200_OK)
def get_users():
    if not users:
        return {"message": "No hay usuarios registrados", "users": []}
    return {"users": users}

# Endpoint para obtener un usuario por su ID (GET)
@app.get("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK)
def get_user(user_id: str):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
