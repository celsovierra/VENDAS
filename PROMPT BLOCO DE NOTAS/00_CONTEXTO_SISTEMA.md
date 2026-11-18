cd /workspaces/VENDAS && cat > "PROMPT BLOCO DE NOTAS/00_CONTEXTO_SISTEMA.md" << 'EOF'
# CONTEXTO: SISTEMA DE GESTÃO DE VENDAS (SHOPEE + MERCADO LIVRE)
Atualizado: 17/11/2026

## Como trabalhar comigo
- Respostas curtas e diretas, UM passo por vez.
- Sempre COMANDO DE TERMINAL (Codespaces), pequeno para não truncar.
- Todo comando que muda arquivo já inclui git add/commit/push.
- Não avançar sem testar a etapa anterior.
- APIs oficiais. Interface moderna e responsiva.
- NUNCA pedir nem colar Secrets/senhas no chat ou em arquivos.

## Objetivo
1 Integrar Shopee e Mercado Livre | 2 Receber vendas | 3 Exibir pedidos/valores/status
4 Etiquetas de envio | 5 Cadastrar produtos e anúncios | 6 Publicar com 1 clique
7 Ligar produto vendido ao fornecedor Temu | 8 Custos, taxas, frete, lucro
9 Compra na Temu manual | 10 Estrutura pronta para automatizar Temu

## Ambiente
- GitHub Codespaces, repo celsovierra/VENDAS (público), /workspaces/VENDAS
- Python venv (.venv), FastAPI + Uvicorn + SQLAlchemy + SQLite (data/vendas.db)
- RODAR NA PORTA 8001: source .venv/bin/activate && uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
- Se "Address already in use": servidor já roda em outro terminal. Reiniciar: pkill -f uvicorn; sleep 2; e rodar de novo
- Painel: https://effective-guide-4j6g5jw7wv5v3qr4j-8001.app.github.dev (Ctrl+F5 após mudanças)
- /config = Configurações | /docs = testes API | /pedidos | /produtos
- Banco NÃO vai para o git. Colunas novas foram criadas via ALTER TABLE só neste Codespace: repetir na VPS.
- Playwright instalado (Chromium) mas a Temu bloqueia (redireciona para login).

## Estrutura
- src/main.py (rotas; tem trechos duplicados antigos de /api/products e ProductIn, limpar depois)
- src/core/database.py, src/core/models.py
- src/web/: index.html, config.html, pedidos.html, produtos.html, layout.js, style.css
- src/mercadolivre/auth.py (router prefix /api/ml: OAuth, token, importar vendas, publicar, categorias, frete)
- src/shopee/ (vazia)

## Banco
- products: id, sku, title, description, cost_price, sale_price, stock, temu_url, temu_supplier, ml_id, images (links separados por vírgula), ml_category, brand, model, weight, length, width, height, shipping_cost, created_at
- orders: id, marketplace, external_id, buyer_name, status, total, marketplace_fee, shipping_cost, product_cost, profit, temu_purchased, temu_order_ref, created_at
- order_items, listings, settings(key,value)

## Rotas prontas
- GET /api/health | GET,POST /api/products | GET,POST /api/orders | GET,POST /api/settings
- GET /api/importar-link?url= (lê título/descrição/imagens por meta tags; Temu devolve só título genérico)
- GET /api/ml/login, /callback, /diag-vendas, /importar-vendas
- GET /api/ml/categorias?q= (sugere categorias ML pelo título)
- GET /api/ml/frete?l&w&h&peso&preco&cat (frete grátis de tabela do ML)
- POST /api/ml/publicar/{id}: HOJE SÓ VALIDA (padrão validar=True), NÃO publica de verdade
  - Envia family_name, categoria, preço, imagens, atributos BRAND/MODEL, shipping me2 free
  - Teste do drone (id 51) deu "TESTE OK com avisos" (sem modo me1; frete grátis obrigatório)
- Função token(db) renova access token automaticamente

## Telas
- /pedidos: lista pedidos (lucro 0 se cancelled), botão Atualizar vendas
- /produtos: lista, botão "+ Novo produto" (SKU, título, descrição, custo, preço, estoque, categoria com "Sugerir pelo título", marca, modelo, peso/medidas/frete opcionais, link Temu, imagens por link), botão "Importar de link", botão amarelo Publicar no ML, botão laranja Comprar (abre link Temu)

## Mercado Livre
- App "mod novo guimod" (GPScell), ID 984001453967681 (Brasil permite só 1 app por conta)
- Conta CELSOVIERRA (434 anúncios). Permissões: publicação/sincronização + vendas leitura
- Redirect URI atual: https://effective-guide-4j6g5jw7wv5v3qr4j-8000.app.github.dev/api/ml/callback (trocar ao mudar de porta/VPS)
- NÃO MEXER na notificação gpscell.site/api-financeiro/webhook/mercadopago (outro sistema)
- SEGURANÇA: Secret apareceu em prints/chat/arquivo. Gerar NOVO (três pontinhos > Renove agora) e salvar só em /config

## Aprendizados
- Temu bloqueia leitura automática (preço/imagem/descrição). Custo e imagens são manuais.
- Descrição própria evita denúncia por cópia no ML (ML só aceita texto simples).
- Frete do ML sai do bolso quando é frete grátis; o real vem no pedido (shipping_cost).
- RISCO: envio direto da Temu ao cliente não passa pelo Mercado Envios e demora 15-40 dias. Conta não tem modo me1. Verificar modos de envio habilitados antes de publicar.

## Progresso
- [x] Banco, modelos, API produtos, painel, pedidos com lucro, /config, OAuth ML, importar vendas, botão Atualizar vendas
- [x] Corrigida rota /pedidos; lucro 0 em cancelado
- [x] Formulário novo produto + importar de link + link Temu + botão Comprar
- [x] Categoria sugerida, marca, modelo, peso/medidas, calcular frete
- [x] Rota publicar ML em modo validação (passou)
- [ ] Verificar modos de envio da conta ML (me1/me2) e viabilidade com Temu
- [ ] Publicar de verdade (passo separado, com confirmação extra)
- [ ] Ajustar título/descrição do produto teste (drone id 51)
- [ ] Frete e custo reais entrando no lucro dos pedidos
- [ ] Botão "Conectar Mercado Livre" no /config
- [ ] Tela listando os 434 anúncios
- [ ] Etiquetas ML | Shopee | Vínculo Temu | Financeiro
- [ ] Upload de imagem do computador (hoje só links)

## Pendências para a VPS
- Proteger rotas /api/* com senha/token (hoje abertas)
- Cron a cada 10 min em /api/ml/importar-vendas
- Trocar Redirect URI do ML para o domínio da VPS
- Recriar colunas novas (ALTER TABLE) no banco da VPS
- importar-vendas não avisa erro do ML (retorna 0): tratar status

## Como usar em novo chat
Colar este arquivo na primeira mensagem e dizer: "Continue de onde parei".
EOF
git add -A && git commit -m "Atualiza contexto" && git push