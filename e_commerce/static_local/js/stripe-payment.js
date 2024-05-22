console.log("Stripe Payment JS is being loaded");

document.addEventListener('DOMContentLoaded', () => {
    const publishKey = document.getElementById('stripe-key').getAttribute('data-publish-key');
    const stripe = Stripe(publishKey);
    let elements;

    initialize();
    document.querySelector("#payment-form").addEventListener("submit", handleSubmit);

    async function initialize() {
        try {
            const response = await fetch("/create-payment-intent", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ items: [{ id: "xl-tshirt", price: 2000 }] }) // Example item data
            });
            const data = await response.json();

            if (!response.ok) throw new Error(data.error || 'Failed to create payment intent');

            console.log("ClientSecret received:", data.clientSecret);
            elements = stripe.elements({ clientSecret: data.clientSecret });

            const cardElement = elements.create("card");
            cardElement.mount("#payment-element");
        } catch (error) {
            console.error("Error:", error.message);
        }
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setLoading(true);

        try {
            const result = await stripe.confirmCardPayment("{clientSecret}", {
                payment_method: {
                    card: elements.getElement('card'),
                    billing_details: {
                        name: 'Fulano de Tal'
                    }
                }
            });

            if (result.error) {
                showMessage(result.error.message);
            } else {
                showMessage("Processing payment...");
            }
        } catch (error) {
            showMessage("An unexpected error occurred.");
            console.error("Error:", error);
        }

        setLoading(false);
    }

    function showMessage(messageText) {
        const messageContainer = document.querySelector("#payment-message");
        messageContainer.textContent = messageText;
        messageContainer.classList.remove("hidden");

        setTimeout(() => messageContainer.classList.add("hidden"), 4000);
    }

    function setLoading(isLoading) {
        const submitButton = document.querySelector("#submit");
        submitButton.disabled = isLoading;
        const spinner = document.querySelector("#spinner");
        const buttonText = document.querySelector("#button-text");

        if (isLoading) {
            submitButton.disabled = true;
            spinner.classList.remove("hidden");
            buttonText.classList.add("hidden");
        } else {
            submitButton.disabled = false;
            spinner.classList.add("hidden");
            buttonText.classList.remove("hidden");
        }
    }
});
