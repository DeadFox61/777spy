from django.utils import timezone
from .models import User


def sign_up(user_login, password, phone, usr_telegram):
    User.objects.create_user(
        user_login,
        password,
        phone=phone,
        usr_telegram=usr_telegram,
        pro_time=timezone.now()
    )