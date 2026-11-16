import requests
from sqlalchemy.orm import Session
from src.core.models import Product
from src.mercadolivre.auth import token as get_token

def importar_ml(db: Session):
    tok = get_token(db)
    if not tok:
        return {"status": "erro", "msg": "Conta do Mercado Livre não conectada."}
    
    headers = {"Authorization": f"Bearer {tok}"}
    
    # 1. Descobre o ID do seu usuário no ML
    user_resp = requests.get("https://api.mercadolibre.com/users/me", headers=headers)
    if user_resp.status_code != 200:
        return {"status": "erro", "msg": f"Erro ao pegar usuário: {user_resp.text}"}
    
    user_id = user_resp.json().get("id")
    
    # 2. Busca os anúncios desse usuário
    resp = requests.get(f"https://api.mercadolibre.com/users/{user_id}/items/search?limit=50", headers=headers)
    if resp.status_code != 200:
        return {"status": "erro", "msg": f"Falha no ML: {resp.text}"}
        
    ids = resp.json().get("results", [])
    salvos = 0
    
    for item_id in ids:
        r = requests.get(f"https://api.mercadolibre.com/items/{item_id}", headers=headers)
        if r.status_code == 200:
            item = r.json()
            sku = item.get("seller_custom_field") or item_id
            title = item.get("title", "")
            price = float(item.get("price", 0))
            stock = int(item.get("available_quantity", 0))
            
            existe = db.query(Product).filter(Product.sku == sku).first()
            if not existe:
                novo = Product(sku=sku, title=title, sale_price=price, cost_price=0.0, stock=stock)
                db.add(novo)
                salvos += 1
            else:
                existe.title = title
                existe.sale_price = price
                existe.stock = stock
                salvos += 1
                
    db.commit()
    return {"status": "ok", "importados": salvos, "total_ml": len(ids)}
