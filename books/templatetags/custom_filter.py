from django import template

register = template.Library()

@register.filter
def make_list(value):
    """Convert a number to a list for looping"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(5)

@register.filter
def pluralize(value):
    """Add 's' for plural"""
    try:
        if int(value) != 1:
            return 's'
        return ''
    except:
        return ''

# Add this for string splitting in templates
@register.filter
def split(value, arg):
    """Split a string by the given argument"""
    return value.split(arg)