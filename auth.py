from datetime import datetime, timedelta, timezone
import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Solo para practica local: en produccion esto va en variables de entorno
SECRET_KEY = "clave-secreta-de-practica-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Usuario de practica (en produccion iria en la base de datos)
USUARIO_DEMO = {
    "username": "admin",
    "hashed_password": bcrypt.hashpw(b"admin123", bcrypt.gensalt()),
}

def verificar_password(password_plano: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password_plano.encode(), hashed_password)

def crear_token_acceso(datos: dict, minutos: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    expira = datetime.now(timezone.utc) + timedelta(minutes=minutos)
    para_codificar = datos.copy()
    para_codificar.update({"exp": expira})
    return jwt.encode(para_codificar, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    error_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise error_credenciales
    except JWTError:
        raise error_credenciales
    return username
