$(document).ready(function () {
    // Intercepta os formulários de adicionar/remover produtos
    const productForm = $(".form-product-ajax");

    productForm.submit(function (event) {
        event.preventDefault();
        const thisForm = $(this);
        const actionEndpoint = thisForm.attr("action");
        const httpMethod = thisForm.attr("method");
        const formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                const submitSpan = thisForm.find(".submit-span");

                // Atualiza o botão com base na resposta
                if (data.added) {
                    submitSpan.html(`
                        <button type="submit" class="btn btn-outline-danger btn-sm w-100">Remover</button>
                    `);
                } else {
                    submitSpan.html(`
                        <button type="submit" class="btn btn-success btn-sm w-100">Adicionar</button>
                    `);
                }

                // Atualiza o número de itens no carrinho no navbar
                const navbarCount = $(".navbar-cart-count");
                navbarCount.text(data.cartItemCount);

                // Atualiza dinamicamente a tabela do carrinho, se necessário
                if (window.location.href.indexOf("cart") !== -1) {
                    refreshCart();
                }
            },
            error: function () {
                $.alert({
                    title: "Erro!",
                    content: "Ocorreu um problema ao processar sua solicitação.",
                    theme: "modern",
                });
            },
        });
    });

    // Atualiza a tabela do carrinho dinamicamente
    function refreshCart() {
        const cartTable = $(".cart-table");
        const cartBody = cartTable.find(".cart-body");
        const refreshCartUrl = "/cart/get-items/";

        $.ajax({
            url: refreshCartUrl,
            method: "GET",
            success: function (data) {
                if (data.items.length > 0) {
                    cartBody.html("");
                    let i = data.items.length;

                    $.each(data.items, function (index, value) {
                        cartBody.append(`
                            <tr class="cart-product">
                                <th scope="row">${i}</th>
                                <td><a href="${value.url}">${value.name}</a></td>
                                <td>${value.quantity}</td>
                                <td>${value.price}</td>
                                <td>${value.total}</td>
                                <td>
                                    <form method="POST" action="/cart/update/" class="form-product-ajax">
                                        <input type="hidden" name="product_id" value="${value.id}">
                                        <input type="number" name="quantity" value="0" class="d-none">
                                        <button type="submit" class="btn btn-danger btn-sm">Remover</button>
                                    </form>
                                </td>
                            </tr>
                        `);
                        i--;
                    });

                    $(".cart-subtotal").text(`R$ ${data.subtotal}`);
                    $(".cart-total").text(`R$ ${data.total}`);
                } else {
                    // Recarrega a página para mostrar o carrinho vazio
                    window.location.href = window.location.href;
                }
            },
            error: function () {
                console.error("Erro ao atualizar o carrinho.");
            },
        });
    }
});
