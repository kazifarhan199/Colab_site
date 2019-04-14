from django import template
from Accounts.models import Github_model

register = template.Library()

@register.simple_tag
def user_repos(user):
    repos = Github_model.objects.filter(user=user).order_by('-stars', 'name')[:5]
    return repos