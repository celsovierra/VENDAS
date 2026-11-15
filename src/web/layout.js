(function(){
const it=[['🏠','Dashboard','/'],['🛒','Pedidos','#'],['📦','Produtos','#'],['📢','Anúncios','#'],['🏷️','Etiquetas','#'],['📊','Financeiro','#'],['👥','Fornecedores','#'],['⚙️','Configurações','/config'],['❓','Ajuda','#'],['🚪','Sair','#']];
const p=location.pathname,n=document.querySelector('nav');if(n)n.remove();
const s=document.createElement('aside');s.id='side';
s.innerHTML='<div class="logo">📍 <b>GPScell <span>Store</span></b><small>Sua loja online, mais fácil!</small></div>'+it.map(i=>`<a href="${i[2]}" class="${i[2]===p?'on':''}"><i>${i[0]}</i>${i[1]}</a>`).join('')+'<div class="stat">● Sistema Online<br><small>'+new Date().toLocaleString('pt-BR')+'</small></div>';
const t=document.createElement('header');t.id='top';
t.innerHTML='<button id="mn" onclick="document.getElementById(\'side\').classList.toggle(\'open\')">☰</button><h2>GPScell <span>Store</span></h2><div>🔔 <b>Administrador</b></div>';
document.body.prepend(s);document.querySelector('main').before(t);
})();
