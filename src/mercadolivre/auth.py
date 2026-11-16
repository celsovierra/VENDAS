import time, httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core import models
router = APIRouter(prefix="/api/ml")
REDIRECT = "https://effective-guide-4j6g5jw7wv5v3qr4j-8000.app.github.dev/api/ml/callback"
def get(db, k):
    r = db.get(models.Setting, k)
    return r.value if r else None
def put(db, k, v):
    r = db.get(models.Setting, k)
    if r: r.value = str(v)
    else: db.add(models.Setting(key=k, value=str(v)))
@router.get("/login")
def login(db: Session = Depends(get_db)):
    a = get(db, "ml_app_id")
    if not a: raise HTTPException(400, "App ID não salvo em /config")
    return RedirectResponse(f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={a}&redirect_uri={REDIRECT}")
@router.get("/callback")
def callback(code: str, db: Session = Depends(get_db)):
    a, s = get(db, "ml_app_id"), get(db, "ml_secret")
    if not a or not s: raise HTTPException(400, "Salve App ID e Secret em /config")
    r = httpx.post("https://api.mercadolibre.com/oauth/token", data={"grant_type": "authorization_code", "client_id": a, "client_secret": s, "code": code, "redirect_uri": REDIRECT}, timeout=30)
    d = r.json()
    if r.status_code != 200: raise HTTPException(400, f"ML recusou: {d.get('message', d)}")
    put(db, "ml_access_token", d["access_token"])
    put(db, "ml_refresh_token", d["refresh_token"])
    put(db, "ml_user_id", d["user_id"])
    put(db, "ml_expires_at", int(time.time()) + int(d["expires_in"]))
    db.commit()
    return HTMLResponse("<h3>Mercado Livre conectado ✓</h3><a href='/config'>Voltar</a>")
