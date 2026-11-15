# CONTEXTO DO PROJETO: GESTÃO DE VENDAS (SHOPEE + MERCADO LIVRE)

## Como trabalhar comigo
- Respostas curtas.
- Sempre enviar em forma de COMANDO DE TERMINAL (colar no Codespaces), um por vez.
- Comandos pequenos para não truncar ao colar.
- Não avançar de etapa sem testar a anterior.
- Usar APIs oficiais das plataformas.
- Interface moderna, profissional e responsiva.

## Objetivo
Centralizar vendas da Shopee e Mercado Livre:
1. Integrar contas Shopee e Mercado Livre
2. Receber vendas automaticamente
3. Exibir pedidos, produtos, valores e status
4. Gerar/imprimir etiquetas de envio
5. Cadastrar produtos e criar anúncios
6. Publicar anúncios nas duas plataformas com um clique
7. Identificar produto vendido e fornecedor na Temu
8. Controlar custos, taxas, fretes e lucro por venda
9. Compra na Temu manual (por enquanto)
10. Estrutura pronta para automatizar compras na Temu no futuro

## Ambiente
- GitHub Codespaces, repositório VENDAS (/workspaces/VENDAS)
- Python 3 + venv em .venv (ativar: source .venv/bin/activate)
- FastAPI + Uvicorn + SQLAlchemy + SQLite (data/vendas.db)
- Rodar API: uvicorn src.main:app --host 0.0.0.0 --port 8000
- Teste: curl localhost:8000/api/health

## Estrutura de pastas
VENDAS/
- PROMPT BLOCO DE NOTAS/   (contexto para novos chats)
- src/main.py              (app FastAPI)
- src/core/database.py     (engine, SessionLocal, Base, get_db)
- src/core/models.py       (Product, Listing, Order, OrderItem)
- src/shopee/              (integração Shopee)
- src/mercadolivre/        (integração Mercado Livre)
- data/vendas.db           (banco SQLite)
- tests/
- .env                     (chaves de API, fora do GitHub)
- requirements.txt

## Tabelas
- products: sku, title, description, cost_price, sale_price, stock, temu_url, temu_supplier
- listings: product_id, marketplace, external_id, status
- orders: marketplace, external_id, buyer_name, status, total, marketplace_fee, shipping_cost, product_cost, profit, temu_purchased, temu_order_ref
- order_items: order_id, product_id, title, quantity, unit_price

## Progresso
- [x] Etapa 1: banco de dados e modelos (testado)
- [x] Etapa 2.1: API base /api/health (testado)
- [ ] Etapa 2.2: rotas de produtos
- [ ] Próximas: painel web, pedidos, integração ML, integração Shopee, etiquetas, anúncios, custos/lucro, Temu

## Como usar em novo chat
Colar este arquivo inteiro na primeira mensagem e dizer: "Continue de onde parei".
