// e_commerce/static_local/js/payment-method.js

document.addEventListener('DOMContentLoaded', function() {
  console.log('=== INICIANDO PAYMENT METHOD JS ===');
  
  const stripeKeyElement = document.getElementById('stripe-key');
  if (!stripeKeyElement) {
    console.error('Elemento stripe-key não encontrado');
    return;
  }
  
  const publishKey = stripeKeyElement.dataset.publishKey;
  if (!publishKey) {
    console.error('Chave pública do Stripe não encontrada');
    return;
  }

  console.log('Chave Stripe encontrada:', publishKey.substring(0, 10) + '...');

  const stripe = Stripe(publishKey);
  let elements;

  // Inicialização
  initialize();
  checkStatus();

  // Event listeners
  const paymentForm = document.querySelector("#payment-form");
  if (paymentForm) {
    paymentForm.addEventListener("submit", handleSubmit);
  }

  // Event listeners para botões de cartões salvos
  document.querySelectorAll('.use-card-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const cardId = this.dataset.cardId;
      const cardName = this.dataset.cardName;
      useSavedCard(cardId, cardName, this);
    });
  });

  // Event listeners para formulários de ação
  document.querySelectorAll('.set-default-form').forEach(form => {
    form.addEventListener('submit', function(e) {
      const btn = this.querySelector('button[type="submit"]');
      setButtonLoading(btn, true);
    });
  });

  document.querySelectorAll('.delete-card-form').forEach(form => {
    form.addEventListener('submit', function(e) {
      const cardName = this.querySelector('button').dataset.cardName;
      if (!confirm(`Tem certeza que deseja remover o cartão ${cardName}?`)) {
        e.preventDefault();
        return;
      }
      const btn = this.querySelector('button[type="submit"]');
      setButtonLoading(btn, true);
    });
  });

  // Função para verificar se deve salvar o cartão
  function shouldSaveCard() {
    const checkbox = document.getElementById('save-card-checkbox');
    const result = checkbox ? checkbox.checked : false;
    console.log('🔍 Verificando se deve salvar cartão:', result);
    return result;
  }

  // Função para usar cartão salvo
  async function useSavedCard(cardId, cardName, button) {
    if (confirm(`Usar o cartão ${cardName} para este pagamento?`)) {
      setButtonLoading(button, true);
      try {
        const response = await fetch('/billing/pay-with-saved-card/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify({
            card_id: cardId
          })
        });
        
        const data = await response.json();
        if (data.success) {
          showMessage("Pagamento processado com sucesso!", false);
          setTimeout(() => {
            window.location.href = "/billing/payment-success/";
          }, 1500);
        } else {
          showMessage(data.error || "Erro ao processar pagamento", true);
          setButtonLoading(button, false);
        }
      } catch (error) {
        console.error('Erro:', error);
        showMessage("Erro inesperado. Tente novamente.", true);
        setButtonLoading(button, false);
      }
    }
  }

  // Inicializar Stripe Elements
  async function initialize() {
    console.log('=== INICIALIZANDO STRIPE ELEMENTS ===');
    try {
      console.log('Fazendo requisição para create-checkout-session...');
      
      const response = await fetch("/billing/create-checkout-session/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie('csrftoken'),
        },
      });
      
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const responseData = await response.json();
      console.log('Response data:', responseData);
      
      if (!responseData.clientSecret) {
        throw new Error('Client secret não recebido');
      }

      const { clientSecret } = responseData;
      
      console.log('Client secret recebido:', clientSecret.substring(0, 20) + '...');

      elements = stripe.elements({ clientSecret });
      const paymentElement = elements.create("payment");
      paymentElement.mount("#payment-element");
      
      console.log('Stripe Elements montado com sucesso');
      
    } catch (error) {
      console.error('Erro ao inicializar:', error);
      showMessage(`Erro ao carregar formulário de pagamento: ${error.message}`, true);
    }
  }

  // Processar submissão do formulário
  async function handleSubmit(e) {
    e.preventDefault();
    console.log('=== PROCESSANDO PAGAMENTO ===');
    setLoading(true);

    try {
      const { error, paymentIntent } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: window.location.origin + "/billing/payment-success/",
        },
        redirect: 'if_required'
      });

      if (error) {
        console.error('Erro no pagamento:', error);
        if (error.type === "card_error" || error.type === "validation_error") {
          showMessage(error.message, true);
        } else {
          showMessage("Ocorreu um erro inesperado.", true);
        }
        setLoading(false);
      } else if (paymentIntent && paymentIntent.status === 'succeeded') {
        console.log('Pagamento bem-sucedido:', paymentIntent.id);
        
        // Verificar se deve salvar o cartão usando a nova função
        if (shouldSaveCard()) {
          console.log('💾 Salvando cartão...');
          await savePaymentMethod(paymentIntent.id);
        } else {
          console.log('⏭️ Não salvando cartão (usuário não marcou)');
        }
        
        showMessage("Pagamento realizado com sucesso!", false);
        setTimeout(() => {
          window.location.href = "/billing/payment-success/";
        }, 2000);
        setLoading(false);
      }
    } catch (error) {
      console.error('Erro ao confirmar pagamento:', error);
      showMessage("Erro inesperado ao processar pagamento", true);
      setLoading(false);
    }
  }

  // Salvar método de pagamento
  async function savePaymentMethod(paymentIntentId) {
    try {
      const response = await fetch('/billing/save-payment-method/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          payment_intent_id: paymentIntentId
        })
      });
      
      const data = await response.json();
      if (data.success && data.card_saved) {
        console.log('✅ Cartão salvo com sucesso');
        showMessage("Cartão salvo com sucesso!", false);
      }
    } catch (error) {
      console.error('❌ Erro ao salvar cartão:', error);
    }
  }

  // Obter cookie CSRF
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

  // Verificar status do pagamento
  async function checkStatus() {
    const clientSecret = new URLSearchParams(window.location.search).get(
      "payment_intent_client_secret"
    );
    
    if (!clientSecret) {
      return;
    }
    
    try {
      const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
      
      switch (paymentIntent.status) {
        case "succeeded":
          showMessage("Pagamento realizado com sucesso!", false);
          break;
        case "processing":
          showMessage("Seu pagamento está sendo processado.", false);
          break;
        case "requires_payment_method":
          showMessage("Seu pagamento não foi bem sucedido, tente novamente.", true);
          break;
        default:
          showMessage("Algo deu errado.", true);
          break;
      }
    } catch (error) {
      console.error('Erro ao verificar status:', error);
    }
  }

  // Exibir mensagens
  function showMessage(messageText, isError = true) {
    const messageContainer = document.querySelector("#payment-message");
    if (messageContainer) {
      messageContainer.textContent = messageText;
      messageContainer.className = isError ? 'alert alert-danger' : 'alert alert-success';
      messageContainer.style.display = "block";
      
      setTimeout(() => {
        messageContainer.style.display = "none";
      }, 5000);
    }
    
    // Log no console também
    if (isError) {
      console.error('❌ Mensagem de erro:', messageText);
    } else {
      console.log('✅ Mensagem de sucesso:', messageText);
    }
  }

  // Controlar loading do botão principal
  function setLoading(isLoading) {
    const submitButton = document.querySelector("#submit");
    const spinner = document.querySelector("#spinner");
    const buttonText = document.querySelector("#button-text");
    
    if (submitButton && buttonText) {
      if (isLoading) {
        submitButton.disabled = true;
        if (spinner) spinner.classList.remove("hidden");
        buttonText.textContent = "Processando...";
      } else {
        submitButton.disabled = false;
        if (spinner) spinner.classList.add("hidden");
        // Recuperar texto original do botão
        const originalText = buttonText.dataset.originalText || 
                           buttonText.textContent.replace("Processando...", "Pagar");
        buttonText.textContent = originalText;
      }
    }
  }

  // Controlar loading de botões específicos
  function setButtonLoading(button, isLoading) {
    const spinner = button.querySelector('.spinner-border');
    const text = button.querySelector('.btn-text');
    
    if (text) {
      if (isLoading) {
        // Salvar texto original
        if (!text.dataset.originalText) {
          text.dataset.originalText = text.textContent;
        }
        button.disabled = true;
        if (spinner) spinner.classList.remove('d-none');
        text.textContent = 'Processando...';
      } else {
        button.disabled = false;
        if (spinner) spinner.classList.add('d-none');
        text.textContent = text.dataset.originalText || text.textContent.replace('Processando...', '');
      }
    }
  }
});