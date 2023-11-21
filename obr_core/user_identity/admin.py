from django.urls import reverse
from django.utils.safestring import mark_safe

from account.models import User


def get_admin_link_for_user_identity(user_identity):
    ct, uid = user_identity.split(":")
    if ct == "account.user" and len(uid) == 8:
        user = User.objects.get(uid=uid)
        url = reverse("admin:account_user_change", args=(user.pk,))
        html = f'<a href="{url}">{user}</a>'
    else:
        html = "<span>anonymous</span>"

    return mark_safe(html)  # NOQA: S308
