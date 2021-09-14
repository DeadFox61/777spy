from .pro_actions import add_pro_days
from .models import PartnerSetting, User, Pay


def make_pay(usr_id, service, amount):
    usr = User.objects.get(id = usr_id)
    if service == '1':
        add_pro_days(usr,1)
    elif service == '2':
        add_pro_days(usr,7)
    elif service == '3':
        add_pro_days(usr,30)


    comment = f'Оплата сервиса {service}'

    referrer = usr.referrer
    if referrer:
        try:
            partner_settings = referrer.partnersetting
        except PartnerSetting.DoesNotExist:
            partner_settings = PartnerSetting(user = referrer)
        ref_back = round(int(amount) * partner_settings.percent / 100)
        partner_settings.balance_current += ref_back
        partner_settings.save()
        comment = f'Оплата сервиса {service}. {ref_back} отчислено пользователю ({referrer.id}){referrer.login}'

    pay = Pay(user = usr, amount = int(amount), comment = comment)
    pay.save()
    return True