from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html

register = template.Library()
user_model = get_user_model()


@register.filter
def author_details(author, current_user):
    # If this isn't a User instance, fail safely
    if not isinstance(author, user_model):
        return ""

    # If this is the currently logged-in user, show "me"
    if author == current_user:
        return format_html("<strong>me</strong>")

    # Otherwise, pick a display name
    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = author.username

    # Wrap name in a safe mailto: link if email exists
    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html("{}{}{}", prefix, name, suffix)
