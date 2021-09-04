import string
import random

from .models import RefLink, Promo
def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    """Генерирует строку для ссылки"""
    return ''.join(random.choice(chars) for _ in range(size))

def add_new_ref_link(usr):
    """Генерирует и добавляет новую реферальную ссылку"""
    new_reflink = RefLink(user=usr,value = id_generator())
    new_reflink.save()
    return {'status':'ok'}

def del_ref_link(usr, ref_value):
    """Удаляет реф ссылку с значением ref_value"""
    RefLink.objects.filter(user = usr, value=ref_value).delete()
    return {'status':'ok'}

def partner_ref_edit_save(usr, ref_value, promo_value, source, comment):
    """Редактирует реферальную ссылку"""
    reflink = RefLink.objects.get(user = usr, value=ref_value)
    reflink.promo = Promo.objects.get(value = promo_value) if promo_value else None
    reflink.source = source
    reflink.comment = comment
    reflink.save()
    return {'status':'ok'}