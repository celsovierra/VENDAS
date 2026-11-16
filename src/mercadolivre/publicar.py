import requests
from sqlalchemy.orm import Session
from src.core.models import Product
from src.mercadolivre.auth import token as get_token

def publicar_no_ml(db: Session, product_id: int):
    tok = get_token(db)
    if not tok:
        return {"status": "erro", "msg": "ML não conectado."}
    
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        return {"status": "erro", "msg": "Produto não encontrado no banco."}
        
    headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
    
    payload = {
        "title": prod.title,
        "category_id": "MLB1744", 
        "price": prod.sale_price,
        "currency_id": "BRL",
        "available_quantity": prod.stock,
        "buying_mode": "buy_it_now",
        "condition": "new",
        "listing_type_id": "gold_special",
        "description": {"plain_text": prod.description or "Sem descrição"},
        "pictures": [{"source": "https://http2.mlstatic.com/D_NQ_NP_2X_711522-MLB50011315137_052022-F.webp"}]
    }
    
    resp = requests.post("https://api.mercadolibre.com/items", headers=headers, json=payload)
    
    if resp.status_code in [200, 201]:
        item = resp.json()
        prod.ml_id = item.get("id")
        db.commit()
        return {"status": "ok", "msg": "Publicado com sucesso!", "id_ml": item.get("id")}
    else:
        return {"status": "erro", "msg": f"Erro ML: {resp.text}"}
