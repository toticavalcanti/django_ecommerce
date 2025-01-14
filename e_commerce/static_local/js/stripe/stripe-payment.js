$(document).ready(function () {
    console.log("Documento pronto");
  
    function initializeStripe() {
        const stripeKeyElement = $("#stripe-key");
  
        if (stripeKeyElement.length === 0) {
            console.error("Elemento stripe-key não encontrado");
            return;
        }
  
        const publishKey = stripeKeyElement.data("publishKey");
  
        if (!publishKey) {
            console.error("Chave pública do Stripe não encontrada");
            return;
        }
  
        const stripe = Stripe(publishKey);
        let elements, cardElement, clientSecret = null;
  
        function initialize() {
            const items = getCartItems();  // Obtém os itens do carrinho
  
            $.ajax({
                url: "/create-payment-intent",
                method: "POST",
                contentType: "application/json",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                data: JSON.stringify({ items: items }),
                success: function (data) {
                    if (data.error) {
                        console.error("Falha ao criar o intent de pagamento:", data.error);
                        return;
                    }
                    clientSecret = data.clientSecret;
  
                    elements = stripe.elements();
                    cardElement = elements.create("card");
                    cardElement.mount("#payment-element");
                    console.log("Elemento do cartão montado");
                },
                error: function (error) {
                    console.error("Erro ao inicializar os elementos do Stripe:", error);
                },
            });
        }
  
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== "") {
                const cookies = document.cookie.split(";");
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === name + "=") {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
  
        function getCartItems() {
            let items = [];
            $.ajax({
                url: "/cart/get-items/",  // Certifique-se que a URL está correta
                method: "GET",
                async: false, // Garante que a requisição seja concluída antes de prosseguir
                success: function (data) {
                    items = data.items;
                },
                error: function (xhr, status, error) {
                    console.error("Erro ao obter itens do carrinho:", error);
                }
            });
            return items;
        }
  
        const paymentForm = $("#payment-form");
  
        if (paymentForm.length > 0) {
            paymentForm.on("submit", function (event) {
                event.preventDefault();
  
                if (!elements || !cardElement) {
                    showMessage("Elemento do cartão não inicializado corretamente.", true);
                    return;
                }
  
                setLoading(true);
  
                stripe
                    .confirmCardPayment(clientSecret, {
                        payment_method: {
                            card: cardElement,
                            billing_details: {
                                // Inclua os detalhes de faturamento se necessário
                            },
                        },
                    })
                    .then(function (result) {
                        if (result.error) {
                            showMessage(result.error.message, true);
                            setTimeout(function () {
                                window.location.href = "/billing/payment-failed/";
                            }, 3000);
                        } else if (result.paymentIntent && result.paymentIntent.status === "succeeded") {
                            showMessage("Pagamento realizado com sucesso!", false);
                            setTimeout(function () {
                                window.location.href = "/billing/payment-success/";
                            }, 3000);
                        } else {
                            showMessage("Pagamento não foi bem-sucedido. Tente novamente.", true);
                            setTimeout(function () {
                                window.location.href = "/billing/payment-failed/";
                            }, 3000);
                        }
                        setLoading(false);
                    })
                    .catch(function (error) {
                        showMessage("Ocorreu um erro inesperado.", true);
                        setTimeout(function () {
                            window.location.href = "/billing/payment-failed/";
                        }, 3000);
                        setLoading(false);
                    });
            });
        } else {
            console.error("Formulário de pagamento não encontrado");
        }
  
        function showMessage(messageText, isError) {
            const messageContainer = $("#payment-message");
            messageContainer.text(messageText).removeClass("hidden");
  
            if (isError) {
                messageContainer.addClass("error-message");
            } else {
                messageContainer.removeClass("error-message");
            }
  
            setTimeout(function () {
                messageContainer.addClass("hidden").text("");
            }, 4000);
        }
  
        function setLoading(isLoading) {
            const submitButton = $("#submit");
            submitButton.prop("disabled", isLoading);
            $("#spinner").toggleClass("hidden", !isLoading);
            $("#button-text").toggleClass("hidden", isLoading);
        }
  
        initialize();
    }
  
    // Inicializa o Stripe diretamente se o elemento estiver presente
    const stripeKeyElement = $("#stripe-key");
  
    if (stripeKeyElement.length > 0) {
        initializeStripe();
    }
  });