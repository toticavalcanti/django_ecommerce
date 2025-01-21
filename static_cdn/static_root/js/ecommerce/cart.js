$(document).ready(function () {
  // Intercepta os formulários de adicionar/remover produtos
  const productForm = $(".form-product-ajax");

  productForm.submit(function (event) {
    event.preventDefault(); // Previne o envio padrão do formulário
    console.log("Formulário interceptado: ", thisForm);
    const thisForm = $(this); // Formulário atual
    const actionEndpoint = thisForm.attr("action"); // URL do formulário
    const httpMethod = thisForm.attr("method"); // Método HTTP
    const formData = thisForm.serialize(); // Dados do formulário

    // Requisição Ajax para adicionar/remover itens
    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function (data) {
        if (data.success) {
          // Atualiza o número de itens no carrinho no navbar
          const navbarCount = $(".navbar-cart-count");
          navbarCount.text(data.cartItemCount);

          // Atualiza os valores de subtotal e total na página
          $(".cart-subtotal").text(`R$ ${data.subtotal}`);
          $(".cart-total").text(`R$ ${data.total}`);

          // Se estamos na página do carrinho
          if (window.location.href.indexOf("cart") !== -1) {
            // Se a quantidade for 0, remove a linha correspondente
            if (thisForm.find('input[name="quantity"]').val() === "0") {
              thisForm.closest("tr").fadeOut(300, function () {
                $(this).remove();
                checkCartEmpty(); // Verifica se o carrinho está vazio
              });
            } else {
              refreshCart(); // Atualiza os dados do carrinho
            }
          } else {
            // Exibe uma mensagem de sucesso (opcional)
            alert("Produto atualizado no carrinho com sucesso!");
          }
        } else {
          // Exibe mensagem de erro se algo der errado
          alert("Erro ao atualizar o carrinho. Tente novamente.");
        }
      },
      error: function (xhr, status, error) {
        console.error("Erro ao processar a requisição:", error);
        alert("Erro ao processar a solicitação. Tente novamente.");
      },
    });
  });

  // Função para atualizar a tabela do carrinho dinamicamente
  function refreshCart() {
    const cartTable = $(".cart-table");
    const cartBody = cartTable.find("tbody");
    const refreshCartUrl = "/cart/get-items/"; // Endpoint para obter itens do carrinho

    $.ajax({
      url: refreshCartUrl,
      method: "GET",
      success: function (data) {
        if (data.items.length > 0) {
          cartBody.html(""); // Limpa a tabela do carrinho
          let i = data.items.length;

          // Itera pelos itens do carrinho e os insere na tabela
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

          // Atualiza os valores de subtotal e total na página
          $(".cart-subtotal").text(`R$ ${data.subtotal}`);
          $(".cart-total").text(`R$ ${data.total}`);
        } else {
          // Recarrega a página para exibir o estado vazio do carrinho
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
      // Recarrega a página se o carrinho estiver vazio
      window.location.href = window.location.href;
    }
  }
});
