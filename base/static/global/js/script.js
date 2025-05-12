document.addEventListener('DOMContentLoaded', function() {
    // Variáveis globais
    const cart = [];
    const cartModal = document.getElementById('cartModal');
    const cartItemsContainer = document.getElementById('cartItems');
    const cartCount = document.querySelector('.cart-count');
    const totalPriceElement = document.querySelector('.total-price');
    const cartBtn = document.querySelector('.cart-btn');
    const closeModalBtn = document.querySelector('.close-modal');
    const checkoutBtn = document.querySelector('.checkout-btn');
    
    // Troca de categorias
    const categoryBtns = document.querySelectorAll('.category-btn');
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Adicionar ao carrinho
    const addToCartBtns = document.querySelectorAll('.add-to-cart');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const menuItem = this.closest('.menu-item');
            const itemId = menuItem.dataset.id || Date.now().toString();
            const itemTitle = menuItem.querySelector('.item-title').textContent;
            const itemPrice = parseFloat(menuItem.querySelector('.item-price').textContent.replace('R$ ', '').replace(',', '.'));
            
            // Verifica se o item já está no carrinho
            const existingItem = cart.find(item => item.id === itemId);
            
            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cart.push({
                    id: itemId,
                    title: itemTitle,
                    price: itemPrice,
                    quantity: 1
                });
            }
            
            updateCart();
            cartModal.classList.add('active');
        });
    });
    
    // Abrir/fechar modal do carrinho
    cartBtn.addEventListener('click', function() {
        cartModal.classList.add('active');
    });
    
    closeModalBtn.addEventListener('click', function() {
        cartModal.classList.remove('active');
    });
    
    // Fechar modal ao clicar fora
    cartModal.addEventListener('click', function(e) {
        if (e.target === cartModal) {
            cartModal.classList.remove('active');
        }
    });
    
    // Finalizar pedido
    checkoutBtn.addEventListener('click', function() {
        if (cart.length > 0) {
            alert('Pedido finalizado com sucesso! Total: ' + calculateTotal().toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'}));
            // Aqui você enviaria os dados para o backend
            cart.length = 0;
            updateCart();
            cartModal.classList.remove('active');
        } else {
            alert('Adicione itens ao carrinho antes de finalizar!');
        }
    });
    
    // Atualizar carrinho
    function updateCart() {
        // Atualizar contador
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
        
        // Atualizar lista de itens
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<div class="empty-cart-message">Seu carrinho está vazio</div>';
        } else {
            cartItemsContainer.innerHTML = '';
            cart.forEach(item => {
                const cartItemElement = document.createElement('div');
                cartItemElement.className = 'cart-item';
                cartItemElement.innerHTML = `
                    <div class="cart-item-info">
                        <div class="cart-item-title">${item.title}</div>
                        <div class="cart-item-price">${item.price.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})}</div>
                        <div class="cart-item-quantity">
                            <button class="quantity-btn minus" data-id="${item.id}">-</button>
                            <span class="quantity-value">${item.quantity}</span>
                            <button class="quantity-btn plus" data-id="${item.id}">+</button>
                            <button class="remove-item" data-id="${item.id}">Remover</button>
                        </div>
                    </div>
                `;
                cartItemsContainer.appendChild(cartItemElement);
            });
        }
        
        // Atualizar total
        totalPriceElement.textContent = calculateTotal().toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
        
        // Adicionar eventos aos botões de quantidade
        document.querySelectorAll('.quantity-btn.minus').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = this.dataset.id;
                const item = cart.find(item => item.id === itemId);
                if (item.quantity > 1) {
                    item.quantity -= 1;
                } else {
                    const itemIndex = cart.findIndex(item => item.id === itemId);
                    cart.splice(itemIndex, 1);
                }
                updateCart();
            });
        });
        
        document.querySelectorAll('.quantity-btn.plus').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = this.dataset.id;
                const item = cart.find(item => item.id === itemId);
                item.quantity += 1;
                updateCart();
            });
        });
        
        document.querySelectorAll('.remove-item').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = this.dataset.id;
                const itemIndex = cart.findIndex(item => item.id === itemId);
                cart.splice(itemIndex, 1);
                updateCart();
            });
        });
    }
    
    // Calcular total
    function calculateTotal() {
        return cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    }
});


const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");

registerBtn.addEventListener("click", () => {
  container.classList.add("active");
});

loginBtn.addEventListener("click", () => {
  container.classList.remove("active");
});