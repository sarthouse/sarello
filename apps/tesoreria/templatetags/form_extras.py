from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Access dict items by variable key: {{ dict|get_item:key }}"""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def dict_lookup(dictionary, key):
    """Access dict items: {{ dict|dict_lookup:key }}"""
    if dictionary is None:
        return None
    return dictionary.get(key, '')
