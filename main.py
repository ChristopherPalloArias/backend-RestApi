from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

# Creación de la instancia de la aplicación FastAPI
app = FastAPI()

# Configuración de los orígenes permitidos para CORS
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://frontendrestapi-3itsj.ondigitalocean.app"
]

# Añadir middleware de CORS para permitir solicitudes desde los orígenes especificados
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],            # Métodos HTTP permitidos
    allow_headers=["*"],            # Encabezados HTTP permitidos
)

# Configuración de la base de datos MySQL
db_config = {
    'host': 'mysql-christopherobin.alwaysdata.net',
    'user': '358042_admin',
    'password': 'YqUZn6T6AxLYc5k',
    'database': 'christopherobin_practiceclientserver'
}

# Modelo de datos para la solicitud de login usando Pydantic
class User(BaseModel):
    username: str
    password: str

# Ruta POST para manejar el login
@app.post("/login")
async def login(user: User):
    # Conexión a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Consulta SQL para verificar las credenciales del usuario
    query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
    cursor.execute(query, (user.username, user.password))
    result = cursor.fetchall()
    
    # Cierre del cursor y la conexión
    cursor.close()
    conn.close()
    
    # Verificación del resultado de la consulta
    if len(result) > 0:
        return {"message": "Login Successfully"}
    else:
        # Lanzar una excepción HTTP 401 si las credenciales son incorrectas
        raise HTTPException(status_code=401, detail="Login Failed")

# Ruta GET para la raíz de la API
@app.get("/")
async def read_root():
    return {"message": "API is working. Use /login to login."}

# Arranque del servidor con Uvicorn si el script se ejecuta directamente
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
