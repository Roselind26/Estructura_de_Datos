# Importamos FastAPI y Pydantic
from fastapi import FastAPI
from pydantic import BaseModel

# Creamos la aplicación FastAPI
app = FastAPI()

# Lista en memoria para almacenar los usuarios (se puede reemplazar por una base de datos)
users = []

# Modelo de usuario usando Pydantic
class User(BaseModel):
    id: int
    name: str
    email: str

# Endpoint para guardar un usuario (POST)
@app.post("/users/")
def create_user(user: User):
    users.append(user)
    return {"message": "Usuario agregado con éxito", "user": user}

# Endpoint para obtener todos los usuarios (GET)
@app.get("/users/")
def get_users():
    return {"users": users}

# Instrucciones para correr el servidor
# 1. Instala FastAPI y Uvicorn si no lo tienes:
#    pip install fastapi uvicorn
# 2. Ejecuta el servidor:
#    uvicorn main:app --reload
# 3. Prueba en http://127.0.0.1:8000/docs para interactuar con los endpoints
