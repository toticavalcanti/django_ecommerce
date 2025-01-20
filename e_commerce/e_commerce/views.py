from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forms import ContactForm

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def home_page(request):
    context = {
                    "title": "Vitrine Digital",
                    "content": "Sua melhor experiência em compras online",
              }
    if request.user.is_authenticated:
        context["premium_content"] = "Você é um usuário Premium"
    return render(request, "home_page.html", context)
    
def about_page(request):
    context = {
                    "title": "Página Sobre",
                    "content": "Bem vindo a página sobre"
              }
    return render(request, "about/view.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
                    "title": "Página de Contato",
                    "content": "Bem vindo a página de contato",
                    "form": contact_form	
              }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if is_ajax(request):
            return JsonResponse({"message": "Obrigado!"})
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if is_ajax(request):
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, "contact/view.html", context)