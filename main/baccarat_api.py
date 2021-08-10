from .models import Baccarat, BaccRule, GlobalSetting, TlgMsgBacc

def get_stats(user):
    """Возвращает всю статистику по баккарам, выбранным у пользователя"""
    bacc_data = []
    baccarats = Baccarat.objects.all().order_by("sort_id")
    selected_baccs = list(user.usersetting.curr_baccarats.all())
    rules = BaccRule.objects.filter(user=user)
    rules_data = []
    for rule in rules:
        rules_data.append({"id": rule.id, "color": rule.color, "rule_type": rule.rule_type, "count": rule.count})
    for baccarat in baccarats:
        if baccarat in selected_baccs:
            bacc_data.append(
                {
                    "is_selected": True,
                    "bacc_id": baccarat.bacc_id,
                    "name": baccarat.name,
                    "stats": baccarat.stats
                }
            )
        else:
            bacc_data.append(
                {
                    "is_selected": False,
                    "bacc_id": baccarat.bacc_id
                }
            )
    return  {
                "bacc_data": bacc_data,
                "rules_data": rules_data
            }

def get_choosen(usr):
    """Возвращает список выбранных баккар"""
    data = {"user": {"is_pro": usr.is_pro}, "baccarats": {"Evolution":[],"Ezugi":[]}}
    selected_baccs = list(usr.usersetting.curr_baccarats.all())
    baccarats = Baccarat.objects.all().order_by("sort_id")
    for baccarat in baccarats:
        data["baccarats"][baccarat.provider].append(
            {
                "bacc_id": baccarat.bacc_id,
                "name": baccarat.name,
                "is_selected": baccarat in selected_baccs
            }
        )
    return data

def change_choise(usr,bacc_id):
    """Включает/выключает выбранную баккару"""
    gl_st = GlobalSetting.objects.get(version = 1000)
    bacc = Baccarat.objects.get(bacc_id=bacc_id)
    if bacc in usr.usersetting.curr_baccarats.all():
        usr.usersetting.curr_baccarats.remove(bacc)
    else:
        if not usr.is_pro and usr.usersetting.curr_baccarats.count() >= gl_st.free_rouls_available:
            return {"status":"err","min_val":gl_st.free_rouls_available}
        usr.usersetting.curr_baccarats.add(bacc)
    return {"status":"ok"}


def add_rule(usr,name,rule_type,count,color):
    """Создаёт и добавляет правило в БД"""
    gl_st = GlobalSetting.objects.get(version = 1000)
    if not usr.is_pro and usr.rule_set.count() >= gl_st.free_rules_available:
        return {"status": "err","min_val":gl_st.free_rules_available}
    rule = BaccRule(
        name=name,
        rule_type=rule_type,
        count=count,
        color=color,
        user=usr
    )
    rule.save()
    return {"status": "ok"}

def get_rules(usr):
    """Возвращает список правил юзера"""
    rules = BaccRule.objects.filter(user=usr)
    data_rules = []
    for rule in rules:
        rule_text = rule.get_text_info()
        data_rules.append(
            {
                "id": rule.id,
                "name": rule_text["name"],
                "rule_type": rule_text["rule_type"],
                "count": rule_text["count"],
                "color": rule_text["color"],
                "is_tg_on": rule.is_tg_on
            }
        )
    return {"rules": data_rules}

def del_rule(rule_id):
    """Удаляет правило"""
    BaccRule.objects.get(id=rule_id).delete()
    return {"status": "ok"}

def get_rule(rule_id):
    """Возвращает правило с id rule_id"""
    rule = BaccRule.objects.get(id=rule_id)
    return  {
                "id": rule.id,
                "name": rule.name,
                "rule_type": rule.rule_type,
                "count": rule.count,
                "color": rule.color
            }
def change_tg(usr,rule_id,is_on):
    """Включает/выключает уведомления в телеграм"""
    rule = BaccRule.objects.get(id=rule_id)
    rule_type = rule.rule_type
    count = rule.count
    gl_st = GlobalSetting.objects.get(version = 1000)
    if not usr.is_pro:
        rule.is_tg_on = False
        TlgMsgBacc.objects.filter(rule=rule).delete()
        rule.save()
        return {"status": "err_pro"}
    else:
        if is_on:
            rule.is_tg_on = True
        else:
            rule.is_tg_on = False
            TlgMsgBacc.objects.filter(rule=rule).delete()
        rule.save()
        return {"status": "ok"}