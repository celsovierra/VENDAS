cd /workspaces/VENDAS && cat > "PROMPT BLOCO DE NOTAS/00_CONTEXTO_SISTEMA.md" << 'EOF'
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
- Rodar: source .venv/bin/activate && uvicorn src.main:app --host 0.0.0.0 --port 8000
- Painel: URL da porta 8000 do Codespace; /config = Configurações; /docs = testes API
- Banco (data/vendas.db) NÃO vai para o git. Subir para VPS sem o banco.

## Estrutura
- src/main.py (rotas), src/core/database.py, src/core/models.py
- src/web/index.html (painel), src/web/config.html (configurações)
- src/mercadolivre/auth.py (OAuth, token, importar vendas)
- src/shopee/ (ainda vazia)
- PROMPT BLOCO DE NOTAS/ (este arquivo), .env (fora do GitHub)

## Banco (tabelas)
- products, listings, settings(key,value)
- orders: id, marketplace, external_id, buyer_name, status, total, marketplace_fee, shipping_cost, product_cost, profit, temu_purchased, temu_order_ref, created_at
- order_items: id, order_id, product_id, title, quantity, unit_price

## Rotas prontas
- GET /api/health
- GET,POST /api/products
- GET,POST /api/orders (lucro = total - taxa - frete - custo)
- GET,POST /api/settings (Secret nunca volta, retorna ***)
- GET / (painel) | GET /config
- GET /api/ml/login (autoriza conta ML)
- GET /api/ml/callback (recebe código e guarda tokens)
- GET /api/ml/diag-vendas (testa permissão de pedidos: status/total/erro)
- GET /api/ml/importar-vendas (importa até 200 pedidos recentes, evita duplicados)
- Função token(db): renova access token automaticamente com refresh_token

## Mercado Livre
- App "mod novo guimod" (nome curto GPScell), ID 984001453967681, criado antes como app Mercado Pago
- Brasil permite só 1 app por conta, por isso foi reaproveitado
- Conta conectada: CELSOVIERRA (434 anúncios visíveis)
- Redirect URI: https://effective-guide-4j6g5jw7wv5v3qr4j-8000.app.github.dev/api/ml/callback
- Fluxos: Authorization Code, Refresh Token
- Permissões: Publicação e sincronização + Vendas/Pedidos (leitura) ativas
- NÃO MEXER na URL de notificação gpscell.site/api-financeiro/webhook/mercadopago (outro sistema em uso)
- Secret antigo apareceu em print: GERAR NOVA (três pontinhos > Renove agora) e salvar só em /config

## Painel (index.html)
- Cards: Produtos, Pedidos, Lucro (lucro ignora pedidos cancelled)
- Botão "Atualizar vendas" ao lado do título Pedidos (chama /api/ml/importar-vendas e recarrega)
- Pedido ML-001 é de teste manual (não existe no ML)

## Progresso
- [x] 1 Banco e modelos
- [x] 2 API produtos
- [x] 3 Painel e cadastro de produtos
- [x] 4 Pedidos com cálculo de lucro
- [x] 5.1 Tela Configurações
- [x] 5.2 Login OAuth Mercado Livre e tokens
- [x] 5.3 Importar vendas do ML (testado: 1 pedido importado, cancelled)
- [x] Botão manual Atualizar vendas
- [ ] Frete e custo do produto entram como 0 (ajustar)
- [ ] Botão "Conectar Mercado Livre" no /config
- [ ] Tela listando os 434 anúncios
- [ ] Etiquetas ML | Integração Shopee | Anúncios 1 clique | Vínculo Temu | Financeiro

## Pendências para a VPS
- Proteger rotas /api/ml/* com senha/token (hoje abertas)
- Cron a cada 10 min chamando /api/ml/importar-vendas
- Trocar Redirect URI do ML para o domínio da VPS
- importar-vendas não avisa erro do ML (retorna 0): tratar status da resposta

## Como usar em novo chat
Colar este arquivo na primeira mensagem e dizer: "Continue de onde parei".
EOF
cat "PROMPT BLOCO DE NOTAS/00_CONTEXTO_SISTEMA.md" | head -5 && git add -A && git commit -m "Atualiza contexto" && git push