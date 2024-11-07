# custom_filters.py
from django import template
import locale

register = template.Library()

@register.filter
def indian_currency_format(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    # Set the locale to 'en_IN' for Indian formatting
    locale.setlocale(locale.LC_NUMERIC, 'en_IN')

    # Format the number using locale.format
    formatted_value = locale.format_string("%d", value, grouping=True)

    # Reset the locale to default
    locale.setlocale(locale.LC_NUMERIC, '')

    return formatted_value
