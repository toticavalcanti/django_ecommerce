from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, FormView, View 
from django.http import HttpResponse
from django.shortcuts import redirect
from .signals import user_logged_in
from django.contrib import messages
from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail

from django.shortcuts import redirect
from django.urls import reverse

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if redirect_path:
            return redirect(redirect_path)
        else:
            return redirect(reverse("accounts:register"))
    return redirect(reverse("accounts:register"))


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'  # Redireciona para a raiz do projeto
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request=self.request, username=email, password=password) 
        if user is not None:
            login(self.request, user)
            user_logged_in.send(sender=user.__class__, instance=user, request=self.request)
            try:
                del self.request.session['guest_email_id']
            except:
                pass
            return redirect(self.success_url)
        else:
            # Mensagem de erro ao usuário
            messages.error(self.request, "Email ou senha inválidos. Tente novamente.")
            return self.form_invalid(form)  # Retorna o formulário com erro

class LogoutView(View):
    """
    View de logout com redirecionamento customizado.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        if request.user.is_authenticated:
            return redirect('/accounts/login/')
        return redirect('/')

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/login/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        # Usando messages.success diretamente
        messages.success(self.request, "Usuário registrado com sucesso! Agora você pode fazer login.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Apenas um método form_invalid
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)
