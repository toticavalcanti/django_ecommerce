$(document).ready(function() {
    console.log("Documento pronto");

    function initializeStripe() {
        console.log("Verificando o elemento stripe-key...");
        const stripeKeyElement = $('#stripe-key');
        console.log("Elemento stripe-key encontrado:", stripeKeyElement);  // Deve imprimir o elemento ou null

        if (stripeKeyElement.length === 0) {
            console.error("Elemento stripe-key não encontrado");
            return;
        }

        const publishKey = stripeKeyElement.data('publishKey');
        console.log("Chave pública do Stripe:", publishKey);

        if (!publishKey) {
            console.error("Chave pública do Stripe não encontrada");
            return;
        }

        const stripe = Stripe(publishKey);
        let elements;
        let cardElement;
        let clientSecret = null;

        function initialize() {
            console.log("Inicializando os Elementos do Stripe");
            $.ajax({
                url: "/create-payment-intent",
                method: "POST",
                contentType: "application/json",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                },
                data: JSON.stringify({ items: [{ id: "xl-tshirt", price: 2000 }] }),
                success: function(data) {
                    if (data.error) {
                        console.error('Falha ao criar o intent de pagamento:', data.error);
                        return;
                    }
                    console.log("ClientSecret recebido:", data.clientSecret);
                    clientSecret = data.clientSecret;

                    // Inicializar os elementos do Stripe e montar o elemento do cartão
                    elements = stripe.elements();
                    cardElement = elements.create("card");
                    cardElement.mount("#payment-element");
                    console.log("Elemento do cartão montado");
                },
                error: function(xhr, status, error) {
                    console.error("Erro ao inicializar os elementos do Stripe:", error);
                }
            });
        }

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const paymentForm = $("#payment-form");
        if (paymentForm.length > 0) {
            paymentForm.on("submit", function(event) {
                event.preventDefault();
                console.log("Evento de submissão capturado");

                if (!elements || !cardElement) {
                    console.error("Elementos não inicializados ou elemento do cartão não montado");
                    showMessage("Elemento do cartão não inicializado corretamente.");
                    return;
                }

                setLoading(true);

                console.log("Confirmando o pagamento com clientSecret:", clientSecret);
                stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: cardElement,
                        billing_details: {
                            // Inclua os detalhes de faturamento se necessário
                        }
                    }
                }).then(function(result) {
                    console.log("Resultado do pagamento:", result);
                    if (result.error) {
                        console.error("Erro ao confirmar o pagamento:", result.error);
                        showMessage(result.error.message);
                    } else {
                        if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                            showMessage("Pagamento realizado com sucesso!");
                            console.log("Pagamento realizado com sucesso! Redirecionando...");

                            // Manter a mensagem visível por 3 segundos antes de redirecionar
                            setTimeout(function() {
                                const nextUrlElement = $('#next-url');
                                const nextUrl = nextUrlElement.data('url') || '/';
                                window.location.href = nextUrl;
                            }, 5000);
                        } else {
                            console.error("Status do pagamento inesperado:", result.paymentIntent.status);
                            showMessage("Pagamento não foi bem-sucedido. Tente novamente.");
                        }
                    }
                    setLoading(false);
                }).catch(function(error) {
                    showMessage("Ocorreu um erro inesperado.");
                    console.error("Erro na promessa de confirmação do pagamento:", error);
                    setLoading(false);
                });
            });
        } else {
            console.error("Formulário de pagamento não encontrado");
        }

        function showMessage(messageText) {
            const messageContainer = $("#payment-message");
            messageContainer.text(messageText).removeClass("hidden");

            // Comentando o setTimeout que oculta a mensagem após 4 segundos
            setTimeout(function() {
                messageContainer.addClass("hidden").text('');
            }, 4000);
        }

        function setLoading(isLoading) {
            const submitButton = $("#submit");
            submitButton.prop('disabled', isLoading);
            const spinner = $("#spinner");
            const buttonText = $("#button-text");

            spinner.toggleClass("hidden", !isLoading);
            buttonText.toggleClass("hidden", isLoading);
        }

        initialize();
    }

    function observeStripeKeyElement() {
        const stripeKeyElement = $('#stripe-key');
        if (stripeKeyElement.length > 0) {
            initializeStripe();
            observer.disconnect();
        }
    }

    const observer = new MutationObserver(function(mutationsList, observer) {
        for (let mutation of mutationsList) {
            if (mutation.type === 'childList' || mutation.type === 'attributes') {
                observeStripeKeyElement();
            }
        }
    });

    observer.observe(document.body, { childList: true, subtree: true, attributes: true });

    observeStripeKeyElement();
});
