from django import template

register = template.Library()

@register.filter
def repeat(value, times):
    """Repeat a string multiple times (for star ratings)"""
    try:
        times = int(times)
        return str(value) * times
    except (ValueError, TypeError):
        return value

# NEW: Filter to create a list of numbers
@register.filter
def make_list(value):
    """Convert a number or string to a list for looping"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(5)  # Default to 5