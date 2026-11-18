(function(){
const l=document.createElement('link');l.rel='stylesheet';l.href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css';document.head.appendChild(l);
const it=[['house','Dashboard','/'],['cart-shopping','Pedidos','/pedidos'],['box','Produtos','/produtos'],['tag','Etiquetas','#'],['chart-simple','Financeiro','#'],['gear','Configurações','/config'],['right-from-bracket','Sair','#']];
const p=location.pathname,n=document.querySelector('nav');if(n)n.remove();
const s=document.createElement('aside');s.id='side';
s.innerHTML='<div class="logo"><span class="pin"><i class="fa-solid fa-car"></i></span><div><b>GPScell</b><b class="az">Store</b></div></div><p class="sub">Sua loja online, mais fácil!</p>'
+it.map(i=>`<a href="${i[2]}" class="${i[2]===p?'on':''}"><i class="fa-solid fa-${i[0]}"></i>${i[1]}${i[3]?'<em>'+i[3]+'</em>':''}</a>`).join('')
+'<div class="stat"><b>● Sistema Online</b><small><i class="fa-regular fa-calendar"></i> '+new Date().toLocaleString('pt-BR',{dateStyle:'short',timeStyle:'short'})+'</small></div>'
+'<div class="promo"><span class="pin"><i class="fa-solid fa-car"></i></span><div><b>GPScell <span class="az">Store</span></b><small>Conectando você com as melhores ofertas!</small></div></div>';
const t=document.createElement('header');t.id='top';
t.innerHTML='<div class="l"><button onclick="document.getElementById(\'side\').classList.toggle(\'open\')"><i class="fa-solid fa-bars"></i></button><h2>GPScell <span class="az">Store</span></h2></div><div class="r"><span class="bell"><i class="fa-regular fa-bell"></i><em>3</em></span><span class="av"><i class="fa-solid fa-user"></i></span><div><b>Administrador ▾</b><small>Bem-vindo(a)!</small></div></div>';
document.body.prepend(s);document.querySelector('main').before(t);
})();
