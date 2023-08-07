from django import template
import string
import random
from datetime import datetime
register = template.Library()


@register.simple_tag
def random_quote():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str


@register.filter
def get_list(the_dict, the_list):
    return the_dict[the_list]


@register.filter
def date_time(value, format="%Y-%m-%d %H:%M"):
    try:
        if type(value) == str:
            return str(datetime.strptime(value, format))
        else:
            return value.strftime(format)
    except Exception as e:
        print("EXCETION: ", e)
        return ''


@register.simple_tag
def have_perm(user, app, action, model):
    perm = f'{app}.{action}_{str(model).lower()}'
    if user.user.has_perm(perm):
        return 'checked'
    return ''


@register.filter
def in_list(value, the_list):
    value = str(value)
    new_list = [int(i) for i in the_list.split(',')]
    return int(value) in new_list


@register.simple_tag
def is_checked(value):
    if (value):
        return "checked"
    return ""


@register.simple_tag
def is_selected(val1, val2):
    if val1 == val2:
        return "selected"
    return ""
