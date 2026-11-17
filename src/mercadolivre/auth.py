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
@router.get("/teste")
def teste(db: Session = Depends(get_db)):
    t, u = get(db, "ml_access_token"), get(db, "ml_user_id")
    if not t: raise HTTPException(400, "Conecte em /api/ml/login")
    h = {"Authorization": f"Bearer {t}"}
    me = httpx.get("https://api.mercadolibre.com/users/me", headers=h, timeout=30).json()
    it = httpx.get(f"https://api.mercadolibre.com/users/{u}/items/search", headers=h, timeout=30).json()
    return {"nome": me.get("nickname"), "anuncios_total": it.get("paging", {}).get("total"), "ids": it.get("results", [])[:5]}
from datetime import datetime
def token(db):
    if int(get(db, "ml_expires_at") or 0) < time.time() + 60:
        r = httpx.post("https://api.mercadolibre.com/oauth/token", data={"grant_type": "refresh_token", "client_id": get(db, "ml_app_id"), "client_secret": get(db, "ml_secret"), "refresh_token": get(db, "ml_refresh_token")}, timeout=30)
        d = r.json()
        if r.status_code != 200: raise HTTPException(400, f"Refresh falhou: {d}")
        put(db, "ml_access_token", d["access_token"]); put(db, "ml_refresh_token", d["refresh_token"]); put(db, "ml_expires_at", int(time.time()) + int(d["expires_in"])); db.commit()
    return get(db, "ml_access_token")
@router.get("/importar-vendas")
def importar(db: Session = Depends(get_db)):
    h = {"Authorization": f"Bearer {token(db)}"}
    u, novos = get(db, "ml_user_id"), 0
    for off in range(0, 200, 50):
        d = httpx.get(f"https://api.mercadolibre.com/orders/search?seller={u}&sort=date_desc&limit=50&offset={off}", headers=h, timeout=30).json()
        for o in d.get("results", []):
            eid = str(o["id"])
            if db.query(models.Order).filter_by(marketplace="mercadolivre", external_id=eid).first(): continue
            fee = sum((i.get("sale_fee") or 0) * i["quantity"] for i in o["order_items"])
            tot = o.get("total_amount") or 0
            ped = models.Order(marketplace="mercadolivre", external_id=eid, buyer_name=(o.get("buyer") or {}).get("nickname"), status=o.get("status"), total=tot, marketplace_fee=fee, shipping_cost=0, product_cost=0, profit=tot - fee, created_at=datetime.fromisoformat(o["date_created"][:19]))
            db.add(ped); db.flush()
            for i in o["order_items"]:
                db.add(models.OrderItem(order_id=ped.id, title=i["item"]["title"], quantity=i["quantity"], unit_price=i["unit_price"]))
            novos += 1
        if len(d.get("results", [])) < 50: break
    db.commit()
    return {"importados": novos}
@router.get("/diag-vendas")
def diag(db: Session = Depends(get_db)):
    h = {"Authorization": f"Bearer {token(db)}"}
    u = get(db, "ml_user_id")
    r = httpx.get(f"https://api.mercadolibre.com/orders/search?seller={u}&limit=1", headers=h, timeout=30)
    d = r.json()
    return {"status": r.status_code, "total": d.get("paging", {}).get("total"), "erro": d.get("message") or d.get("error")}


@router.post("/publicar/{pid}")
def publicar(pid: int, db: Session = Depends(get_db), validar: bool = True):
    p = db.get(models.Product, pid)
    if not p:
        raise HTTPException(404, "Produto nao encontrado")
    imgs = [x.strip() for x in (p.images or "").split(",") if x.strip()]
    if not imgs:
        return {"msg": "Falta imagem: cole ao menos 1 link de imagem no produto."}
    t = token(db)
    h = {"Authorization": "Bearer " + t}
    cat = p.ml_category
    if not cat:
        r = httpx.get("https://api.mercadolibre.com/sites/MLB/domain_discovery/search", params={"q": p.title, "limit": 1}, headers=h, timeout=30)
        d = r.json() if r.status_code == 200 else []
        if not d:
            return {"msg": "Nao achei categoria para este titulo."}
        cat = d[0]["category_id"]
    body = {
        "family_name": p.title[:60], "category_id": cat, "price": p.sale_price,
        "currency_id": "BRL", "available_quantity": p.stock or 1,
        "buying_mode": "buy_it_now", "condition": "new",
        "listing_type_id": "gold_special",
        "shipping": {"mode": "me2", "free_shipping": True},
        "pictures": [{"source": u} for u in imgs],
        "attributes": [{"id": "BRAND", "value_name": p.brand or "Genérica"}, {"id": "MODEL", "value_name": p.model or "Padrão"}],
    }
    url = "https://api.mercadolibre.com/items/validate" if validar else "https://api.mercadolibre.com/items"
    r = httpx.post(url, json=body, headers=h, timeout=60)
    if r.status_code in (200, 201, 204):
        if validar:
            return {"msg": "TESTE OK: categoria " + cat + ". O ML aceitou os dados (nada foi publicado)."}
        p.ml_id = r.json().get("id"); p.ml_category = cat; db.commit()
        return {"msg": "Publicado! ID: " + str(p.ml_id)}
    try:
        cs = r.json().get("cause", [])
    except Exception:
        cs = []
    if validar and cs and all(c.get("type") == "warning" for c in cs):
        return {"msg": "TESTE OK com avisos: " + " | ".join(c.get("message", "") for c in cs) + ". Nada foi publicado."}
    return {"msg": "ML recusou (" + str(r.status_code) + "): " + r.text[:2500]}


@router.get("/categorias")
def categorias(q: str, db: Session = Depends(get_db)):
    h = {"Authorization": "Bearer " + token(db)}
    r = httpx.get("https://api.mercadolibre.com/sites/MLB/domain_discovery/search", params={"q": q, "limit": 5}, headers=h, timeout=30)
    d = r.json() if r.status_code == 200 else []
    return [{"id": x["category_id"], "nome": x.get("category_name", "")} for x in d]
