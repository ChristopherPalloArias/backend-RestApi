from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Configuración de la base de datos
db_config = {
    'host': 'mysql-christopherobin.alwaysdata.net',
    'user': '358042_admin',
    'password': 'YqUZn6T6AxLYc5k',
    'database': 'christopherobin_practiceclientserver'
}

# Modelo de datos para la solicitud de login
class User(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(user: User):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
    cursor.execute(query, (user.email, user.password))
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if len(result) > 0:
        return {"message": "Login Successfully"}
    else:
        raise HTTPException(status_code=401, detail="Login Failed")

@app.get("/")
async def read_root():
    return {"message": "API is working. Use /login to login."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
