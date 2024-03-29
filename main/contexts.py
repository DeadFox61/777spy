from .models import Roulette, Baccarat, PartnerSetting, GlobalSetting
from . import langs 
from django.conf import settings
from hashlib import md5

def get_fk_sign(merchant_id, secret_word, order_id, order_amount, currency = 'RUB'):
    sign_string = f'{merchant_id}:{order_amount}:{secret_word}:{order_id}'
    print(sign_string)
    return md5(sign_string.encode('utf-8')).hexdigest()

def get_main_page_context(usr):
    """Возвращает контекст для основной страницы с статистикой"""
    gl_settings = GlobalSetting.objects.get(version = 1000)
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
            'free_roul_count': gl_settings.free_rouls_available,
            'free_rule_count': gl_settings.free_rules_available
        },
        'text': langs.ru,
        'site_msg':gl_settings.site_msg,
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
    gl_settings = GlobalSetting.objects.get(version = 1000)
    context = {
        'user_id': usr.id,
        'user_mail': usr.login,
        'price_day': gl_settings.price_day,
        'price_week': gl_settings.price_week,
        'price_month': gl_settings.price_month,
        'order_ids': {
            '1':str(usr.id)+'_1',
            '2':str(usr.id)+'_2',
            '3':str(usr.id)+'_3'
        },
        'fk_merchant_id': settings.PAY_ID

    }
    signs = {
            '1':get_fk_sign(context["fk_merchant_id"], settings.PAY_SECRET1, context["order_ids"]["1"], context["price_day"]),
            '2':get_fk_sign(context["fk_merchant_id"], settings.PAY_SECRET1, context["order_ids"]["2"], context["price_week"]),
            '3':get_fk_sign(context["fk_merchant_id"], settings.PAY_SECRET1, context["order_ids"]["3"], context["price_month"])
    }
    context["signs"] = signs
    return context