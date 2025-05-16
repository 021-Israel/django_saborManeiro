// Dentro da função AJAX de adicionar/remover
setTimeout(() => {
    atualizarCarrinho();
}, 500);  // Um pequeno delay pode garantir que as mudanças sejam refletidas.


location.reload();  // Recarregar a página para refletir as mudanças





document.querySelectorAll('.increase-qty').forEach(button => {
    button.addEventListener('click', async function() {
        const itemId = this.getAttribute('data-item-id');
        await atualizarQuantidade(itemId, 1);  // Aguarda até que a quantidade seja alterada
        await atualizarCarrinho(); // Atualiza o carrinho com as novas informações
    });
});

document.querySelectorAll('.decrease-qty').forEach(button => {
    button.addEventListener('click', async function() {
        const itemId = this.getAttribute('data-item-id');
        await atualizarQuantidade(itemId, -1);
        await atualizarCarrinho();
    });
});

document.querySelectorAll('.remove-item').forEach(button => {
    button.addEventListener('click', async function() {
        const itemId = this.getAttribute('data-item-id');
        await removerDoCarrinho(itemId);
        await atualizarCarrinho();  // Atualiza o carrinho após remoção
    });
});



