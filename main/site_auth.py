from django.utils import timezone
from .models import User, RefLink, ClickEntry
from .pro_actions import add_pro_days

from django.db import IntegrityError

def sign_up(user_login, password, phone, usr_telegram, refid):
    referrer = None
    reflink = None
    promo = None
    free_days = 0
    if refid:
        reflink = RefLink.objects.filter(value=refid).first()
        if reflink:
            referrer = reflink.user
            promo = reflink.promo
    if promo:
        free_days = promo.free_days
    user = User.objects.create_user(
        user_login,
        password,
        phone = phone,
        usr_telegram = usr_telegram,
        pro_time = timezone.now(),
        referrer = referrer,
        referrer_link = reflink
    )
    add_pro_days(user,free_days)

def add_click(refid, ip):
    reflink = RefLink.objects.filter(value=refid).first()
    if reflink:
        click = ClickEntry(link = reflink, ip = ip)
        try:
            click.save()
        except IntegrityError:
            pass
        
