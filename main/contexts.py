from .models import Roulette, Baccarat
from . import langs 

# Возвращает контекст для основной страницы с статистикой
def get_main_page_context(usr):
    roulettes = Roulette.objects.all().order_by("roul_id")
    baccarats = Baccarat.objects.all().order_by("sort_id")
    tg_bot = ''
    if usr.tlg_id and usr.is_pro:
        tg_bot = usr.get_bot().name
    context = {
        'user': {
            'login': usr.login,
            'phone': usr.phone,
            'telegram': usr.usr_telegram,
            'tlg_id': usr.tlg_id,
            'tg_bot': tg_bot,
            'is_pro': usr.is_pro,
            'pro_time': usr.pro_time
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