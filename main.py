from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, Producto
from auth import USUARIO_DEMO, verificar_password, crear_token_acceso, obtener_usuario_actual

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Satélite API")

class ProductoCrear(BaseModel):
    nombre: str
    precio: float
    existencia: int = 0

class ProductoRespuesta(ProductoCrear):
    id: int

@app.get("/")
def root():
    return {"mensaje": "API ERP Satélite funcionando"}

@app.get("/salud")
def salud():
    return {"estado": "ok", "base_datos": "erp_demo"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != USUARIO_DEMO["username"] or not verificar_password(form_data.password, USUARIO_DEMO["hashed_password"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = crear_token_acceso({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@app.get("/productos/{producto_id}", response_model=ProductoRespuesta)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{producto_id}", response_model=ProductoRespuesta)
def actualizar_producto(producto_id: int, datos: ProductoCrear, db: Session = Depends(get_db), usuario: str = Depends(obtener_usuario_actual)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.nombre = datos.nombre
    producto.precio = datos.precio
    producto.existencia = datos.existencia
    db.commit()
    db.refresh(producto)
    return producto

@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db), usuario: str = Depends(obtener_usuario_actual)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return None

@app.post("/productos", status_code=201, response_model=ProductoRespuesta)
def crear_producto(datos: ProductoCrear, db: Session = Depends(get_db), usuario: str = Depends(obtener_usuario_actual)):
    nuevo = Producto(**datos.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
