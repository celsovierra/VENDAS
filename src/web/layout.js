document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.createElement('div');
    sidebar.className = 'sidebar';
    sidebar.innerHTML = `
        <div class="logo">
            <div class="logo-icon"><i class="fa-solid fa-location-dot"></i></div>
            <div class="logo-text">GPScell<br><span>Store</span></div>
        </div>
        <div class="nav">
            <a href="/" class="${window.location.pathname === '/' ? 'on' : ''}"><i class="fa-solid fa-house"></i> Dashboard</a>
            <a href="/pedidos" class="${window.location.pathname === '/pedidos' ? 'on' : ''}"><i class="fa-solid fa-cart-shopping"></i> Pedidos</a>
            <a href="/produtos" class="${window.location.pathname === '/produtos' ? 'on' : ''}"><i class="fa-solid fa-box"></i> Produtos</a>
            <a href="/anuncio"><i class="fa-solid fa-bullhorn"></i> Anúncios</a>
            <a href="#"><i class="fa-solid fa-tag"></i> Etiquetas</a>
            <a href="#"><i class="fa-solid fa-chart-simple"></i> Financeiro</a>
            <a href="#"><i class="fa-solid fa-users"></i> Fornecedores</a>
            <a href="/config"><i class="fa-solid fa-gear"></i> Configurações</a>
            <a href="#"><i class="fa-solid fa-circle-question"></i> Ajuda</a>
            <a href="#"><i class="fa-solid fa-right-from-bracket"></i> Sair</a>
        </div>
        <div class="status-box">
            <div class="status-online"><span class="dot"></span> Sistema Online</div>
            <div class="status-date">16/11/2026, 12:55</div>
        </div>
        <div class="bottom-box">
            <i class="fa-solid fa-car"></i>
            <div>GPScell Store<br><small>Conectando você com as melhores ofertas!</small></div>
        </div>
    `;

    const container = document.querySelector('.layout');
    if (container) {
        container.prepend(sidebar);
    }
});
