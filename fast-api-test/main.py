from fastapi import FastAPI, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
import uvicorn
from model.user_conn import UserConnection
from schema.user_schema import UserSchema

# Creamos una instancia de FastAPI
app = FastAPI()
conn = UserConnection()

# Definimos una ruta que será invocada con el método GET al ingresar al path /
@app.get("/", status_code=HTTP_200_OK)
def root():
    return {"response":"Hola, soy una API de FastAPI"}

@app.get("/api/users", status_code=HTTP_200_OK)
def root_api():
    items = []
    for data in conn.read_all():
        dictionary = {}
        dictionary['id'] = data[0]
        dictionary['name'] = data[1]
        dictionary['phone'] = data[2]
        items.append(dictionary)
    return items

@app.get("/api/user/{id}", status_code=HTTP_200_OK)
def get_one(id:str):
    item = {}
    data = conn.read_one(id)
    item['id'] = data[0]
    item['name'] = data[1]
    item['phone'] = data[2]
    return item

@app.post("/api/insert", status_code=HTTP_201_CREATED)
def insert(user_data:UserSchema):
    data = user_data.dict()
    data.pop("id")
    print(data)
    conn.write(data)
    return Response(status_code=HTTP_201_CREATED)

@app.put("/api/update/{id}", status_code=HTTP_204_NO_CONTENT)
def update(user_data: UserSchema, id:str):
    data = user_data.dict()
    data["id"] = id
    conn.update(data)
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.delete("/api/delete/{id}", status_code=HTTP_204_NO_CONTENT)
def delete(id:str):
    conn.delete(id)
    return Response(status_code=HTTP_204_NO_CONTENT)

# Si estamos ejecutando este archivo como script principal, iniciamos el servidor de aplicación web
if __name__ == '__main__':
    # Iniciamos el servidor en el host 127.0.0.1:8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)