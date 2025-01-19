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
        if (data.success) {
          // Atualiza o número de itens no carrinho no navbar
          const navbarCount = $(".navbar-cart-count");
          navbarCount.text(data.cartItemCount);

          // Atualiza o subtotal e total na página
          $(".cart-subtotal").text(`R$ ${data.subtotal}`);
          $(".cart-total").text(`R$ ${data.total}`);

          // Se estamos na página do carrinho
          if (window.location.href.indexOf("cart") !== -1) {
            // Se a quantidade for 0, remove a linha
            if (thisForm.find('input[name="quantity"]').val() === "0") {
              thisForm.closest("tr").fadeOut(300, function () {
                $(this).remove();
                checkCartEmpty(); // Verifica se o carrinho está vazio
              });
            } else {
              refreshCart();
            }
          }
        }
      },
      error: function () {
        alert("Erro ao processar a solicitação. Tente novamente.");
      },
    });
  });

  // Função para atualizar a tabela do carrinho dinamicamente
  function refreshCart() {
    const cartTable = $(".cart-table");
    const cartBody = cartTable.find("tbody");
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

  // Verifica se o carrinho está vazio e atualiza a interface
  function checkCartEmpty() {
    if ($(".cart-product").length === 0) {
      window.location.href = window.location.href; // Recarrega a página para mostrar o estado vazio
    }
  }
});
