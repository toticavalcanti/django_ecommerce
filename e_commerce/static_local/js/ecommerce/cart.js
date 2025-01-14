$(document).ready(function () {
    // Cart + Add Product
    const productForm = $(".form-product-ajax");

    productForm.submit(function (event) {
        event.preventDefault();
        const thisForm = $(this);
        const actionEndpoint = thisForm.attr("data-endpoint");
        const httpMethod = thisForm.attr("method");
        const formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                const submitSpan = thisForm.find(".submit-span");
                if (data.added) {
                    submitSpan.html(`
                        <button type='submit' class='btn btn-outline-danger btn-sm w-100'>Remover</button>
                    `);
                } else {
                    submitSpan.html(`
                        <button type='submit' class='btn btn-success btn-sm w-100'>Adicionar</button>
                    `);
                }

                const navbarCount = $(".navbar-cart-count");
                navbarCount.text(data.cartItemCount);

                const currentPath = window.location.href;
                if (currentPath.indexOf("cart") !== -1) {
                    refreshCart();
                }
            },
            error: function () {
                $.alert({
                    title: "Oops!",
                    content: "Ocorreu um erro, tente novamente mais tarde!",
                    theme: "modern",
                });
            },
        });
    });

    function refreshCart() {
        const cartTable = $(".cart-table");
        const cartBody = cartTable.find(".cart-body");
        const productsRow = cartBody.find(".cart-product");
        const currentUrl = window.location.href;
        const refreshCartUrl = "/cart/get-items/";
        const refreshCartMethod = "GET";

        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            success: function (data) {
                const hiddenCartItemRemoveForm = $(".cart-item-remove-form");
                if (data.items.length > 0) {
                    productsRow.html("");
                    let i = data.items.length;
                    $.each(data.items, function (index, value) {
                        const newCartItemRemove = hiddenCartItemRemoveForm.clone();
                        newCartItemRemove.css("display", "block");
                        newCartItemRemove.find(".cart-item-product-id").val(value.id);
                        cartBody.prepend(
                            `<tr>
                                <th scope="row">${i}</th>
                                <td><a href="${value.url}">${value.name}</a></td>
                                <td>${value.quantity}</td>
                                <td>${value.price}</td>
                                <td>${value.total}</td>
                                <td>${newCartItemRemove.html()}</td>
                             </tr>`
                        );
                        i--;
                    });
                    cartBody.find(".cart-subtotal").text(data.subtotal);
                    cartBody.find(".cart-total").text(data.total);
                } else {
                    window.location.href = currentUrl;
                }
            },
            error: function () {
                console.error("Erro ao atualizar o carrinho.");
            },
        });
    }
});