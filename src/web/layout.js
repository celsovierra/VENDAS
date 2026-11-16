const menu = [
    ['house','Dashboard','/'],
    ['cart-shopping','Pedidos','/pedidos'],
    ['box','Produtos','/produtos'],
    ['bullhorn','Anúncios','/anuncio'],
    ['tag','Etiquetas','#'],
    ['chart-simple','Financeiro','#'],
    ['users','Fornecedores','#'],
    ['gear','Configurações','/config'],
    ['circle-question','Ajuda','#'],
    ['right-from-bracket','Sair','#']
];

document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('.nav');
    if (!nav) return;
    nav.innerHTML = '';
    
    menu.forEach(item => {
        const a = document.createElement('a');
        a.href = item[2];
        a.innerHTML = `<i class="fa-solid fa-${item[0]}"></i> ${item[1]}`;
        if (window.location.pathname === item[2]) {
            a.className = 'on';
        }
        nav.appendChild(a);
    });
});
