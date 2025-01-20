from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Multiplica o valor (value) pelo argumento (arg).
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add_class(field, css_class):
    """
    Adiciona uma classe CSS a um campo de formulário.
    """
    try:
        return field.as_widget(attrs={"class": css_class})
    except AttributeError:
        return field
