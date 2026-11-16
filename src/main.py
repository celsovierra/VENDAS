from fastapi import FastAPI
from src.core.database import engine, Base
from src.core import models

Base.metadata.create_all(engine)
app = FastAPI(title="Gestão de Vendas")
from src.mercadolivre.auth import router as ml_router
app.include_router(ml_router)

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

class OrderIn(BaseModel):
    marketplace: str
    external_id: str
    buyer_name: str = ""
    status: str = "pago"
    total: float = 0
    marketplace_fee: float = 0
    shipping_cost: float = 0
    product_cost: float = 0

@app.get("/api/orders")
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).order_by(models.Order.id.desc()).all()

@app.post("/api/orders")
def create_order(o: OrderIn, db: Session = Depends(get_db)):
    obj = models.Order(**o.model_dump())
    obj.profit = o.total - o.marketplace_fee - o.shipping_cost - o.product_cost
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

class SettingIn(BaseModel):
    key: str
    value: str

@app.get("/api/settings")
def get_settings(db: Session = Depends(get_db)):
    rows = db.query(models.Setting).all()
    return {r.key: ("***" if ("secret" in r.key.lower() or "token" in r.key.lower()) else r.value) for r in rows}

@app.post("/api/settings")
def save_setting(s: SettingIn, db: Session = Depends(get_db)):
    row = db.get(models.Setting, s.key)
    if row: row.value = s.value
    else: db.add(models.Setting(key=s.key, value=s.value))
    db.commit()
    return {"ok": True}

@app.get("/config", include_in_schema=False)
def config_page():
    return FileResponse("src/web/config.html")

@app.get("/pedidos", include_in_schema=False)
@app.get("/produtos", include_in_schema=False)
def produtos_page():
    return FileResponse("src/web/produtos.html?v=2")

def pedidos_page():
    return FileResponse("src/web/pedidos.html")

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="src/web"), name="static")


@app.get("/api/ml/importar-produtos")
def importar_produtos_ml(db: Session = Depends(get_db)):
    from src.mercadolivre.importar_produtos import importar_ml
    return importar_ml(db)
