from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import CreateView, FormView, View 
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import url_has_allowed_host_and_scheme
from .signals import user_logged_in

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail


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

            # Remove o email de convidado da sessão, se existir
            self.request.session.pop('guest_email_id', None)

            # Verifica se há um parâmetro `next` válido na URL
            next_url = self.request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
                return redirect(next_url)

        return super(LoginView, self).form_valid(form)

# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#                     "form": form
#               }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request, username=username, password=password) 
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if url_has_allowed_host_and_scheme( redirect_path, request.get_host() ):
#                 return redirect( redirect_path )
#             else:
#                 # Redireciona para uma página de sucesso.
#                 return redirect("/")
#         else:
#             #Retorna uma mensagem de erro de 'invalid login'.
#             print("Login inválido")
#     return render(request, "accounts/login.html", context)

class LogoutView(View):
    template_name = 'accounts/logout.html'
    
    def get(self, request, *args, **kwargs):
        context = {
            "content": "Você efetuou o logout com sucesso! :)"
        }
        logout(request)
        return render(request, self.template_name, context)
    
# def logout_page(request):
#     context = {
#                 "content": "Você efetuou o logout com sucesso! :)"
#               }
#     logout(request)
#     return render(request, "accounts/logout.html", context)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#                 "form": form
#               }
#     if form.is_valid():
#         form.save()
#     return render(request, "accounts/register.html", context)