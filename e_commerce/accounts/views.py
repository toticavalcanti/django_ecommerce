from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import LoginForm, RegisterForm
def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
                    "form": form
              }
    print("User logged in")
    print(request.user.is_authenticated)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password) 
        print(user)
        print(request.user.is_authenticated)
        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            if url_has_allowed_host_and_scheme( redirect_path, request.get_host() ):
                return redirect( redirect_path )
            else:
                # Redireciona para uma página de sucesso.
                return redirect("/")
        else:
            #Retorna uma mensagem de erro de 'invalid login'.
            print("Login inválido")
    return render(request, "accounts/login.html", context)

def logout_page(request):
    context = {
                "content": "Você efetuou o logout com sucesso! :)"
              }
    logout(request)
    return render(request, "accounts/logout.html", context)

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
                    "form": form
              }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    return render(request, "accounts/register.html", context) 