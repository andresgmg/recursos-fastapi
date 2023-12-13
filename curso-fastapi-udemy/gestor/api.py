from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, constr, validator
import database as db
import helpers


class ModelCliente(BaseModel):
    dni: constr(min_length=3, max_length=3)
    nombre: constr(min_length=2, max_length=30)
    apellido: constr(min_length=2, max_length=30)


class ModelCrearCliente(ModelCliente):
    @validator("dni")
    def validar_dni(cls, dni):
        if helpers.dni_valido(dni, db.Clientes.lista):
            return dni
        else:
            raise ValueError("Cliente ya existente o DNI incorrecto!")


app = FastAPI()


@app.get("/")
async def index():
    content = {"mensaje": "¡Hola mundo!"}
    return JSONResponse(content=content)


@app.get("/html/", response_class=HTMLResponse)
async def html():
    content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>¡Hola mundo!</title>
    </head>
    <body>
        <h1>¡Hola mundo!</h1>
    </body>
    </html>
    """
    return content


@app.get("/clientes/")
async def clientes():
    content = [
        {
            "dni": cliente.dni,
            "nombre": cliente.nombre.encode("latin-1").decode("utf-8"),
            "apellido": cliente.apellido.encode("latin-1").decode("utf-8"),
        }
        for cliente in db.Clientes.lista
    ]
    return JSONResponse(content=content)


@app.get("/clientes/buscar/{dni}")
async def clientes_buscar(dni: str):
    cliente = db.Clientes.buscar(dni=dni)
    if cliente:
        cliente_serializable = {
            "dni": cliente.dni,
            "nombre": cliente.nombre.encode("latin-1").decode("utf-8"),
            "apellido": cliente.apellido.encode("latin-1").decode("utf-8"),
        }
        return JSONResponse(content=cliente_serializable)
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado!")


@app.post("/clientes/crear/")
async def clientes_crear(datos: ModelCrearCliente):
    cliente = db.Clientes.crear(datos.dni, datos.nombre, datos.apellido)
    if cliente:
        cliente_serializable = {
            "dni": cliente.dni,
            "nombre": cliente.nombre.encode("latin-1").decode("utf-8"),
            "apellido": cliente.apellido.encode("latin-1").decode("utf-8"),
        }
        return JSONResponse(content=cliente_serializable, status_code=201)
    else:
        raise HTTPException(status_code=400, detail="Cliente no creado!")


print("Servidor de la API...")
