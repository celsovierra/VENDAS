cd /workspaces/VENDAS && cat > "PROMPT BLOCO DE NOTAS/00_CONTEXTO_SISTEMA.md" << 'EOF'
# CONTEXTO: SISTEMA DE GESTÃO DE VENDAS (SHOPEE + MERCADO LIVRE)
Atualizado: 18/11/2026

## Como trabalhar comigo
- Respostas curtas e diretas, UM passo por vez.
- Sempre COMANDO DE TERMINAL (Codespaces), pequeno para não truncar.
- Todo comando que muda arquivo já inclui git add/commit/push.
- Não avançar sem testar a etapa anterior.
- APIs oficiais. Interface moderna e responsiva.
- NUNCA pedir nem colar Secrets/senhas no chat ou em arquivos.
- NUNCA escrever no arquivo de contexto sem eu pedir.
- No terminal, não usar o caractere de exclamação dentro de comandos (o bash quebra). Usar Python para editar arquivos.
- Não colocar endereços/URLs sozinhos dentro de blocos de comando.

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
- Páginas: / | /config | /docs (testes API) | /pedidos | /produtos | /anuncios
- Porta 8001 deve estar Pública na aba PORTAS do VS Code.
- Banco NÃO vai para o git. Colunas novas foram criadas via ALTER TABLE só neste Codespace: repetir na VPS.
- Playwright instalado (Chromium) mas a Temu bloqueia (redireciona para login).
- Cache: layout.js está em ?v=16. Ao mudar o menu, subir o número em todas as páginas html.

## Estrutura
- src/main.py (rotas; tem trechos duplicados antigos de /api/products e ProductIn, limpar depois)
- src/core/database.py, src/core/models.py
- src/web/: index.html, config.html, pedidos.html, produtos.html, anuncios.html, layout.js, style.css
- src/mercadolivre/auth.py (router prefix /api/ml)
- src/shopee/ (vazia, ainda sem código)
- Menu (layout.js): Dashboard, Pedidos, Produtos, Anúncios ML, Etiquetas, Financeiro, Configurações, Sair. Removidos: Fornecedores e Ajuda.

## Banco
- products: id, sku, title, description, cost_price, sale_price, stock, temu_url, temu_supplier, ml_id, images (links separados por vírgula), ml_category, brand, model, weight, length, width, height, shipping_cost, created_at
- orders: id, marketplace, external_id, buyer_name, status, total, marketplace_fee, shipping_cost, product_cost, profit, temu_purchased, temu_order_ref, created_at
- order_items, listings, settings(key,value)
- Chaves em settings: ml_app_id, ml_secret, ml_access_token, ml_refresh_token, ml_user_id, ml_expires_at, shopee_partner_id, shopee_partner_key, shopee_shop_id

## Rotas prontas
- GET /api/health | GET,POST /api/products | GET,POST /api/orders | GET,POST /api/settings
- GET /api/importar-link?url= (lê título/descrição/imagens por meta tags; Temu devolve só título genérico)
- GET /api/ml/login, /callback, /teste, /diag-vendas, /importar-vendas
- GET /api/ml/diag-envio (só leitura: modos de envio da conta)
- GET /api/ml/anuncios?offset= (lista os 434 anúncios, 20 por página)
- GET /api/ml/categorias?q= (sugere categorias ML pelo título)
- GET /api/ml/frete?l&w&h&peso&preco&cat (frete grátis de tabela do ML)
- POST /api/ml/publicar/{id}: HOJE SÓ VALIDA (padrão validar=True), NÃO publica de verdade
- POST /api/shopee/publicar/{id}: AINDA NÃO EXISTE (o botão mostra aviso)
- Função token(db) renova access token automaticamente

## Telas
- /pedidos: lista pedidos (lucro 0 se cancelled), botão Atualizar vendas
- /produtos: lista, "+ Novo produto", "Importar de link". Botões por linha: ML amarelo (publicar no ML; vira "ML ✔" quando já publicado), S laranja (Shopee), Comprar verde (abre link do fornecedor). Cores com !important no estilo inline.
- /anuncios: tabela dos anúncios do ML (ID, título, preço, estoque, status, link), paginação 20 em 20
- /config: cartão Mercado Livre (App ID, Secret) e cartão Shopee (Partner ID, Partner Key, Shop ID)

## Mercado Livre
- App "mod novo guimod" (GPScell), ID 984001453967681 (Brasil permite só 1 app por conta)
- Conta CELSOVIERRA (434 anúncios). Permissões: publicação/sincronização + vendas leitura
- REDIRECT no código (auth.py linha 8): porta 8001. O Redirect URI no painel do ML ainda está na porta 8000 (NÃO foi alterado). Para o login funcionar de novo, os dois precisam ser iguais.
- NÃO MEXER na notificação gpscell.site/api-financeiro/webhook/mercadopago (outro sistema)
- SEGURANÇA: Secret apareceu em prints/chat/arquivo. Gerar NOVO (três pontinhos > Renove agora) e salvar só em /config

## Resultado: modos de envio da conta ML (18/11/2026)
- Modos habilitados: me2 (drop_off, padrão e obrigatório), custom, not_specified. NÃO tem me1.
- Frete grátis é padrão no país todo (custo sai do bolso do vendedor).
- Conclusão: venda direta Temu -> cliente final NÃO é viável de forma limpa.
- Caminho seguro: comprar na Temu com entrega no meu endereço, receber, embalar, etiquetar e despachar via me2.
- Prazo do cliente = prazo Temu (15-40 dias) + envio ML. Atraso prejudica reputação.
- Custom pode ser testado, mas depende de categoria/condições.

## Shopee
- Cartão em /config pronto. App ainda NÃO criado em open.shopee.com.
- Plano: src/shopee/auth.py (/api/shopee), assinatura HMAC-SHA256, login/callback, token com renovação, pedidos, etiquetas, publicar.
- Diferenças: imagens precisam ser enviadas (upload), e não existe modo validar.

## Aprendizados
- Temu bloqueia leitura automática (preço/imagem/descrição). Custo e imagens são manuais.
- Descrição própria evita denúncia por cópia no ML (ML só aceita texto simples).
- Frete do ML sai do bolso quando é frete grátis; o real vem no pedido (shipping_cost).
- Conta ML tem só 1 pedido (cancelado); /orders/{id}/shipments dá 404 para cancelado. Frete real só testável com venda real.
- importar-vendas só importa pedidos novos (não atualiza status) e não liga item ao produto.

## Progresso
- [x] Banco, modelos, API produtos, painel, pedidos com lucro, /config, OAuth ML, importar vendas, botão Atualizar vendas
- [x] Formulário novo produto + importar de link + link Temu + botão Comprar
- [x] Categoria sugerida, marca, modelo, peso/medidas, calcular frete
- [x] Rota publicar ML em modo validação (passou)
- [x] Verificar modos de envio da conta ML (diag-envio)
- [x] Tela listando os 434 anúncios (/anuncios)
- [x] Menu limpo; cartão Shopee em /config; botões ML/S/Comprar
- [ ] Criar app Shopee e fazer integração (login, pedidos, etiquetas, publicar)
- [ ] Frete e custo reais no lucro dos pedidos (esperar primeira venda real)
- [ ] Atualizar status dos pedidos já importados; ligar item vendido ao produto
- [ ] Publicar de verdade no ML (passo separado, com confirmação extra)
- [ ] Ajustar título/descrição do produto teste (drone id 51)
- [ ] Botão "Conectar Mercado Livre" no /config
- [ ] Etiquetas ML | Vínculo Temu | Financeiro
- [ ] Upload de imagem do computador (hoje só links)
- [ ] Limpar código duplicado do main.py

## Pendências para a VPS
- Proteger rotas /api/* com senha/token (hoje abertas)
- Cron a cada 10 min em /api/ml/importar-vendas
- Trocar Redirect URI do ML para o domínio da VPS
- Recriar colunas novas (ALTER TABLE) no banco da VPS
- importar-vendas não avisa erro do ML (retorna 0): tratar status

## Como usar em novo chat
Colar este arquivo na primeira mensagem e dizer: "Continue de onde parei".
EOF
git add -A && git commit -m "Atualiza contexto" ; git push