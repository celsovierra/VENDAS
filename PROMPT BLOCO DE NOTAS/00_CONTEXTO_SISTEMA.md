cat > "PROMPT BLOCO DE NOTAS/00_CONTEXTO_SISTEMA.md" << 'EOF'
# CONTEXTO: SISTEMA DE GESTÃO DE VENDAS (SHOPEE + MERCADO LIVRE)

## Como trabalhar comigo
- Respostas curtas, UM passo por vez.
- Sempre em COMANDO DE TERMINAL (Codespaces), pequeno para não truncar.
- Todo comando que abrir área de teste já inclui git add/commit/push.
- Não avançar sem testar a etapa anterior.
- APIs oficiais. Interface moderna e responsiva.
- Nunca pedir nem colar Secrets no chat.

## Objetivo
1 Integrar Shopee e Mercado Livre | 2 Receber vendas | 3 Exibir pedidos/valores/status
4 Etiquetas de envio | 5 Cadastrar produtos e anúncios | 6 Publicar com 1 clique
7 Ligar produto vendido ao fornecedor Temu | 8 Custos, taxas, frete, lucro
9 Compra na Temu manual | 10 Estrutura pronta para automatizar Temu

## Ambiente
- GitHub Codespaces, repo celsovierra/VENDAS (/workspaces/VENDAS)
- Python venv (.venv), FastAPI + Uvicorn + SQLAlchemy + SQLite (data/vendas.db)
- Rodar: uvicorn src.main:app --host 0.0.0.0 --port 8000
- Painel: URL da porta 8000 do Codespace; /config = Configurações; /docs = testes API

## Estrutura
- src/main.py (rotas), src/core/database.py, src/core/models.py
- src/web/index.html (painel), src/web/config.html (configurações)
- src/shopee/, src/mercadolivre/ (integrações, ainda vazias)
- PROMPT BLOCO DE NOTAS/ (este arquivo), .env (fora do GitHub)

## Banco (tabelas)
products, listings, orders, order_items, settings(key,value)

## Rotas prontas
GET /api/health | GET,POST /api/products | GET,POST /api/orders (lucro = total - taxa - frete - custo)
GET,POST /api/settings (Secret nunca volta, retorna ***) | GET / | GET /config

## Mercado Livre
- App "mod novo guimod" (nome curto GPScell), ID 984001453967681, criado antes como app Mercado Pago
- Brasil permite só 1 app por conta, por isso foi reaproveitado e configurado para Mercado Livre
- Redirect URI: https://effective-guide-4j6g5jw7wv5v3qr4j-8000.app.github.dev/api/ml/callback
- Fluxos marcados: Authorization Code, Refresh Token. Permissões: leitura/escrita
- NÃO MEXER na URL de notificação gpscell.site/api-financeiro/webhook/mercadopago (outro sistema em uso)
- Secret anterior apareceu em print: GERAR NOVA (três pontinhos > Renove agora) e salvar só em /config

## Progresso
- [x] 1 Banco e modelos
- [x] 2 API produtos
- [x] 3 Painel e cadastro de produtos
- [x] 4 Pedidos com cálculo de lucro
- [x] 5.1 Tela Configurações (App ID e Secret no sistema)
- [ ] 5.2 Login OAuth Mercado Livre (/api/ml/login e /api/ml/callback) e guardar tokens
- [ ] 5.3 Importar vendas do ML automaticamente
- [ ] Etiquetas ML | Integração Shopee | Anúncios 1 clique | Vínculo Temu | Financeiro

## Como usar em novo chat
Colar este arquivo na primeira mensagem e dizer: "Continue de onde parei".
EOF
cat "PROMPT BLOCO DE NOTAS/00_CONTEXTO_SISTEMA.md" && git add -A && git commit -m "Atualiza contexto" && git push