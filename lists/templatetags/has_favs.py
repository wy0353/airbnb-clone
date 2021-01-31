from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def has_favs(context):
    user = context.request.user
    has_favs = user.list.rooms.exists()
    return has_favs
