document.addEventListener("DOMContentLoaded", function () {
    const stripeKeyElement = document.getElementById("stripe-key");
    if (!stripeKeyElement) {
        console.error("Elemento stripe-key não encontrado");
        return;
    }

    const publishKey = stripeKeyElement.getAttribute("data-publish-key");
    if (!publishKey) {
        console.error("Chave pública do Stripe não encontrada");
        return;
    }

    const stripe = Stripe(publishKey);
    const form = document.getElementById("payment-form");
    const submitButton = document.getElementById("submit");
    const paymentMessage = document.getElementById("payment-message");

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await fetch("/billing/create-checkout-session", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            });

            if (!response.ok) {
                throw new Error("Erro ao criar sessão de pagamento");
            }

            const { sessionId } = await response.json();
            const { error } = await stripe.redirectToCheckout({
                sessionId: sessionId
            });

            if (error) {
                throw error;
            }
        } catch (error) {
            showError(error.message);
        }
        setLoading(false);
    }

    function showError(message) {
        paymentMessage.style.display = "block";
        paymentMessage.textContent = message;
        setTimeout(() => {
            paymentMessage.style.display = "none";
            paymentMessage.textContent = "";
        }, 4000);
    }

    function setLoading(isLoading) {
        submitButton.disabled = isLoading;
        submitButton.textContent = isLoading ? "Processando..." : "Pagar";
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    if (form) {
        form.addEventListener("submit", handleSubmit);
    }
});