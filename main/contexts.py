from .models import Roulette, Baccarat, PartnerSetting
from . import langs 
from django.conf import settings

def get_main_page_context(usr):
    """Возвращает контекст для основной страницы с статистикой"""
    roulettes = Roulette.objects.all().order_by("roul_id")
    baccarats = Baccarat.objects.all().order_by("sort_id")
    tg_bot = ''
    if usr.tlg_id and usr.get_is_pro():
        tg_bot = usr.get_bot().name
    context = {
        'user': {
            'login': usr.login,
            'phone': usr.phone,
            'telegram': usr.usr_telegram,
            'tlg_id': usr.tlg_id,
            'tg_bot': tg_bot,
            'is_pro': usr.get_is_pro(),
            'pro_time': usr.pro_time,
            'fav_nums': usr.usersetting.checked_nums
        },
        'roulettes': [
            {
                'is_evol': roul.roul_id < 30,
                'name': roul.name,
                'id': roul.roul_id,
                "count": roul.number_set.count()
            }
            for roul in roulettes
        ],
        'baccarats': {
            "EG":[
                {
                    'provider': bacc.provider,
                    'name': bacc.name,
                    'id': bacc.bacc_id
                }
                for bacc in baccarats if bacc.provider == "Evolution"
            ],
            "Ezugi":[
                {
                    'provider': bacc.provider,
                    'name': bacc.name,
                    'id': bacc.bacc_id
                }
                for bacc in baccarats if bacc.provider == "Ezugi"
            ]
        },
        'settings': {
            'free_roul_count': 1,
            'free_rule_count': 3
        },
        'text': langs.ru,
        'range37': range(37),
        'range11': range(1, 12),
        'range12': range(1, 13)
    }
    return context

def get_partner_page_context(usr):
    """Возвращает контекст для страницы партнёра"""
    try:
        partner_settings = usr.partnersetting
    except PartnerSetting.DoesNotExist:
        partner_settings = PartnerSetting(user = usr)
        partner_settings.save()
    promos = partner_settings.curr_promo.all().order_by("id")
    reflinks = usr.reflink_set.all().order_by("id")
    context = {
        'text': langs.ru,
        'stats': {
            'balance_current': partner_settings.balance_current,
            'balance_wait': partner_settings.balance_wait,
            'balance_paid': partner_settings.balance_paid,
            'balance_all': partner_settings.balance_current + partner_settings.balance_wait + partner_settings.balance_paid,
            'clicks_count': partner_settings.get_clicks_count(),
            'reg_count': partner_settings.get_reg_count()
        },
        'promos': [
            {
                'id': promo.id,
                'value': promo.value,
                'free_days': promo.free_days
            }
            for promo in promos
        ],
        'reflinks': [
            {
                'id': reflink.id,
                'value': reflink.value,
                'clicks_count': reflink.get_clicks_count(),
                'reg_count': reflink.get_reg_count(),
                'promo_value': reflink.promo.value if reflink.promo else '',
                'source': reflink.source,
                'comment': reflink.comment
            }
            for reflink in reflinks

        ],
        'url': 'https://'+settings.URL
    }
    return context

def get_pro_page_context(usr):
    """Возвращает контекст для страницы оплаты"""
    context = {
        'user_id': usr.id,
        'user_mail': usr.login,
        'price_day': 1000,
        'price_week': 5000,
        'price_month': 15000,
        'order_id': usr.id,
        'fk_merchant_id': settings.PAY_ID,

    }
    return context