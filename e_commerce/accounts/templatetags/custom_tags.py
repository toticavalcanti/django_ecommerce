from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    Adiciona uma classe CSS a um campo de formulário.
    """
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css_class})
    # Caso o campo não seja válido, retorna o campo original.
    return field
