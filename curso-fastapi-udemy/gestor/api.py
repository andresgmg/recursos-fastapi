from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import database as db

json_headers = {"content-type":"application/json; charset=utf-8"}

app = FastAPI()

@app.get("/")
async def index():
    content = {"mensaje": "¡Hola mundo!"}
    return JSONResponse(content=content)

@app.get("/html/")
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
    return Response(content=content, media_type="text/html")

@app.get("/clientes")
async def clientes():
    content = [
        {'dni': cliente.dni, 'nombre': cliente.nombre, 'apellido': cliente.apellido} for cliente in db.Clientes.lista
    ]
    return JSONResponse(content=content, headers=json_headers)

print("Servidor de la API...")