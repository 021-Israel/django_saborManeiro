// function getCSRFToken() {
//   return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
// }


// document.addEventListener("DOMContentLoaded", function() {
//     const cartBtn = document.querySelector(".cart-btn");
//     const cartModal = document.getElementById("cartModal");
//     const closeModal = document.querySelector(".close-modal");
//     const cartCount = document.querySelector(".cart-count");
//     const cartItemsContainer = document.getElementById("cartItems");
//     const totalPrice = document.querySelector(".total-price");

    

//     function atualizarCarrinho() {
//         fetch("/carrinho/")
//         .then(response => response.json())
//         .then(data => {
//             cartItemsContainer.innerHTML = "";
//             if (Object.keys(data.itens).length === 0) {
//                 cartItemsContainer.innerHTML = "<div class='empty-cart-message'>Seu carrinho está vazio</div>";
//             } else {
//                 for (let id in data.itens) {
//                     let item = data.itens[id];
//                     cartItemsContainer.innerHTML += `
//                         <div class="cart-item">
//                             <strong>${item.nome}</strong> - R$${item.preco.toFixed(2)} x ${item.quantidade}
//                             <button onclick="removerDoCarrinho('${id}')">Remover</button>
//                         </div>
//                     `;
//                 }
//             }
//             cartCount.textContent = data.total_itens;
//             totalPrice.textContent = `R$ ${data.total.toFixed(2)}`;
//         });
//     }

//     cartBtn.addEventListener("click", () => {
//         cartModal.style.display = "block";
//         atualizarCarrinho();
//     });

//     closeModal.addEventListener("click", () => {
//         cartModal.style.display = "none";
//     });

//     window.removerDoCarrinho = function(produtoId) {
//         fetch("/remover/", {
//             method: "POST",
//             headers: {'X-CSRFToken': getCSRFToken()},
//             body: new URLSearchParams({produto_id: produtoId})
//         })
//         .then(() => atualizarCarrinho());
//     };

//     function getCSRFToken() {
//         return document.querySelector('[name=csrfmiddlewaretoken]').value;
//     }

    
// });




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
    
    // Atualizar carrinho
    function updateCart() {
        // Atualizar contador
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
        
        // Atualizar lista de itens
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<div class="empty-cart-message">Seu carrinho está vazio</div>';
        } else {
            cart.forEach(item => {
                let cartItemElement = document.getElementById(`cart-item-${item.id}`);
                
                // Se o item não existir no DOM, crie-o
                if (!cartItemElement) {
                    cartItemElement = document.createElement('div');
                    cartItemElement.id = `cart-item-${item.id}`;
                    cartItemElement.className = 'cart-item';
                    
                    const cartItemHTML = `
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
                    cartItemElement.innerHTML = cartItemHTML;
                    cartItemsContainer.appendChild(cartItemElement);
                }

                // Atualiza a quantidade do item se já estiver no DOM
                cartItemElement.querySelector('.quantity-value').textContent = item.quantity;
                cartItemElement.querySelector('.cart-item-price').textContent = item.price.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
            });

            // Remover itens que não estão mais no carrinho
            const allItemElements = cartItemsContainer.querySelectorAll('.cart-item');
            allItemElements.forEach(element => {
                const itemId = element.id.replace('cart-item-', '');
                if (!cart.find(item => item.id === itemId)) {
                    element.remove();
                }
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









//Login e cadastre-se
const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");

registerBtn.addEventListener("click", () => {
  container.classList.add("active");
});

loginBtn.addEventListener("click", () => {
  container.classList.remove("active");
});



// Troca de categoria
document.querySelectorAll('.category-btn').forEach(button => {
    button.addEventListener('click', function () {
      const categoria = this.dataset.categoria;
      const url = categoria ? `?categoria=${categoria}` : window.location.pathname;
      window.location.href = url;
    });
  });