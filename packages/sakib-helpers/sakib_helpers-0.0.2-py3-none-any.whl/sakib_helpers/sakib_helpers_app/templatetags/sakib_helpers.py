from django import template

register = template.Library()

# @register.tag
# def highlight_code(parser, token):
#     code = token.split_contents()[-1]
#     nodelist = parser.parse(('endcode',))
#     parser.delete_first_token()
#     return CodeNode(code, nodelist)


@register.filter()
def upperCase(value):
    return str(value).upper()
