from fastapi import FastAPI
from src.core.database import engine, Base
from src.core import models

Base.metadata.create_all(engine)
app = FastAPI(title="Gestão de Vendas")

@app.get("/api/health")
def health():
    return {"status": "ok"}

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.core.database import get_db

class ProductIn(BaseModel):
    sku: str
    title: str
    description: str = ""
    cost_price: float = 0
    sale_price: float = 0
    stock: int = 0
    temu_url: str = ""
    temu_supplier: str = ""

@app.get("/api/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/api/products")
def create_product(p: ProductIn, db: Session = Depends(get_db)):
    if db.query(models.Product).filter_by(sku=p.sku).first():
        raise HTTPException(400, "SKU já existe")
    obj = models.Product(**p.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.core.database import get_db

class ProductIn(BaseModel):
    sku: str
    title: str
    description: str = ""
    cost_price: float = 0
    sale_price: float = 0
    stock: int = 0
    temu_url: str = ""
    temu_supplier: str = ""

@app.get("/api/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/api/products")
def create_product(p: ProductIn, db: Session = Depends(get_db)):
    if db.query(models.Product).filter_by(sku=p.sku).first():
        raise HTTPException(400, "SKU já existe")
    obj = models.Product(**p.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

from fastapi.responses import FileResponse
@app.get("/", include_in_schema=False)
def home():
    return FileResponse("src/web/index.html")
