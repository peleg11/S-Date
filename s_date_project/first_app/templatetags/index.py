from django import template
from first_app.models import Post, Account
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.simple_tag
def liked_by_user(post_id, user_id):
    if Post.objects.get(pk=post_id).likes.filter(id=user_id).exists():
        return True
    else:
        return False
@register.simple_tag
def liked_user(user_id, user):
    if Account.objects.get(pk=user_id).likes.filter(id=user).exists():
        return True
    else:
        return False
@register.simple_tag
def block_user(user_id, user):
    if Account.objects.get(pk=user).blocked.filter(id=user_id).exists():
        return True
    else:
        return False
@register.simple_tag
def shown_user(user_id, user):
    if user_id==user:
        return True
    else:
        return False

@register.simple_tag
def is_block_user(user_id, user):
    if Account.objects.get(pk=user_id).blocked.filter(id=user).exists():
        return user
