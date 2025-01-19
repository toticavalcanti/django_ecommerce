from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import CreateView, FormView, View 
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import url_has_allowed_host_and_scheme
from .signals import user_logged_in
from django.contrib import messages
from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail
from django.contrib import messages

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email       = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")

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
        return super(LoginView, self).form_valid(form)

class LogoutView(View):
    template_name = 'accounts/logout.html'
    
    def get(self, request, *args, **kwargs):
        context = {
            "content": "Você efetuou o logout com sucesso! :)"
        }
        logout(request)
        return render(request, self.template_name, context)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'  # Redireciona para a página de login após o registro

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuário registrado com sucesso! Agora você pode fazer login.')
        return response
