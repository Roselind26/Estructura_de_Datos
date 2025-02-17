import uuid
import re  # Importamos re para validar el email
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, EmailStr, Field

# Creamos la aplicación FastAPI
app = FastAPI(
    title="Sistema de Usuarios",
    description="API para gestión de usuarios",
    version="1.0.0"
)

# Base de datos en memoria
users = []

# Modelo de usuario con validaciones
class User(BaseModel):
    name: str
    email: EmailStr  # Validación automática de email
    username: str = Field(..., min_length=3, description="Debe tener al menos 3 caracteres")

@app.post("/users/", tags=["Users"], status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    # Validar si el email tiene formato correcto (opcional porque ya usamos EmailStr)
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, user.email):
        raise HTTPException(status_code=400, detail="Formato de email inválido")

    # Verificar si ya existe un usuario con el mismo email o username
    for existing_user in users:
        if existing_user["email"] == user.email or existing_user["username"] == user.username:
            raise HTTPException(status_code=400, detail="El usuario ya existe con este email o username")

    # Si no existe, agregarlo con un ID único
    new_user = {"id": str(uuid.uuid4()), **user.dict()}
    users.append(new_user)
    return {"message": "Usuario agregado con éxito", "user": new_user}

@app.get("/users/", tags=["Users"], status_code=status.HTTP_200_OK)
def get_users():
    if not users:
        return {"message": "No hay usuarios registrados", "users": []}
    return {"users": users}

@app.get("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK)
def get_user(user_id: str):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
