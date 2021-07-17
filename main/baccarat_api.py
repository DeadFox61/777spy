from .models import Baccarat, BaccRule, GlobalSetting

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