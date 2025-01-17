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