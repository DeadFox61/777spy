from .models import Roulette, Rule, GlobalSetting, TlgMsg

def get_stats(user):
    """Возвращает статистику рулеток"""
    roul_data = []
    roulettes = Roulette.objects.all().order_by("roul_id")
    selected_rouls = list(user.usersetting.curr_roulettes.all())
    is_zero = user.usersetting.is_zero
    ind_stats = user.usersetting.individual_stats
    rules = Rule.objects.filter(user=user)
    rules_data = []
    for rule in rules:
        rules_data.append({"id": rule.id, "color": rule.color, "rule_type": rule.rule_type, "is_in_order": rule.is_in_row, "count": rule.how_many_in_row})
    for roulette in roulettes:
        if roulette in selected_rouls:
            roul_data.append(
                {
                    "is_selected": True,
                    "roul_id": roulette.roul_id,
                    "name": roulette.name,
                    "nums": [
                        {
                            "num": i.num,
                            "is_zero": i.is_zero(),
                            "is_red": i.is_red()
                        }
                        for i in roulette.number_set.all().order_by("id").reverse()[:150]
                    ],
                    "stats": roulette.new_stats,
                    "ind_stats": ind_stats.get(str(roulette.roul_id)),
                    "count": roulette.number_set.count()
                }
            )
        else:
            roul_data.append(
                {
                    "is_selected": False,
                    "roul_id": roulette.roul_id
                }
            )
    return {
            "roul_data": roul_data,
            "is_zero": is_zero,
            "rules_data": rules_data
        }

def get_choosen(usr):
    data = {"user": {"is_pro": usr.get_is_pro()}, "roulettes": []}
    selected_rouls = list(usr.usersetting.curr_roulettes.all())
    roulettes = Roulette.objects.all().order_by("roul_id")
    for roulette in roulettes:
        data["roulettes"].append(
            {
                "roul_id": roulette.roul_id,
                "name": roulette.name,
                "is_selected": roulette in selected_rouls
            }
        )
    return data

def change_choise(usr,roul_id):
    gl_st = GlobalSetting.objects.get(version = 1000)
    roul = Roulette.objects.get(roul_id=roul_id)
    if roul in usr.usersetting.curr_roulettes.all():
        usr.usersetting.curr_roulettes.remove(roul)
    else:
        if not usr.get_is_pro() and usr.usersetting.curr_roulettes.count() >= gl_st.free_rouls_available:
            return {"status":"err","min_val":gl_st.free_rouls_available}
        usr.usersetting.curr_roulettes.add(roul)
    return {"status":"ok"}

def get_zeros(usr):
    return usr.usersetting.is_zero

def change_zero(usr,zr_name):
    is_zero = usr.usersetting.is_zero
    if is_zero[zr_name]:
        is_zero[zr_name] = 0
    else:
        is_zero[zr_name] = 1
    usr.usersetting.is_zero = is_zero
    usr.usersetting.save()
    return {"status": "ok"}


def add_rule(usr, name, is_in_row, rule_type, count, max_count, color):
    """Создаёт и добавляет правило в БД"""
    gl_st = GlobalSetting.objects.get(version = 1000)
    if not usr.get_is_pro() and usr.rule_set.count() >= gl_st.free_rules_available:
        return {"status": "err","min_val":gl_st.free_rules_available}
    rule = Rule(
        name=name,
        is_in_row=is_in_row,
        rule_type=rule_type,
        how_many_in_row=count,
        max_count=max_count,
        color=color,
        user=usr
    )
    rule.save()
    return {"status": "ok"}

def get_rules(usr):
    """Возвращает список правил юзера"""
    rules = Rule.objects.filter(user=usr)
    data_rules = []
    for rule in rules:
        rule_text = rule.get_text_info()
        data_rules.append(
            {
                "id": rule.id,
                "name": rule_text["name"],
                "category": rule_text["category"],
                "rule_type": rule_text["rule_type"],
                "how_many_in_row": rule_text["how_many_in_row"],
                "max_count": "-"+str(rule.max_count) if rule.max_count!=9999 and rule.get_category()!=0 else "",
                "color": rule_text["color"],
                "is_tg_on": rule.is_tg_on
            }
        )
    return {"rules": data_rules}

def del_rule(rule_id):
    """Удаляет правило с id rule_id"""
    Rule.objects.get(id=rule_id).delete()
    return {"status": "ok"}

def get_rule(rule_id):
    """Возвращает правило с id rule_id в виде json"""
    rule = Rule.objects.get(id=rule_id)
    return  {
                "id": rule.id,
                "name": rule.name,
                "is_in_row": rule.is_in_row,
                "category": rule.get_category(),
                "rule_type": rule.rule_type,
                "how_many_in_row": rule.how_many_in_row,
                "max_count": rule.max_count,
                "color": rule.color
            }
def change_tg(usr,rule_id,is_on):
    """Включает/выключает уведомления в телеграм для правила с id rule_id"""
    rule = Rule.objects.get(id=rule_id)
    rule_type = rule.rule_type
    how_many_in_row = rule.how_many_in_row
    gl_st = GlobalSetting.objects.get(version = 1000)
    if not usr.get_is_pro():
        rule.is_tg_on = False
        TlgMsg.objects.filter(rule=rule).delete()
        rule.save()
        return {"status": "err_pro"}
    else:
        if is_on:
            if rule_type == 1 or rule_type == 2 or rule_type == 3:
                if how_many_in_row < gl_st.min_chances:
                    return {"status": "err","min_val":gl_st.min_chances}
            elif rule_type == 4 or rule_type == 5:
                if how_many_in_row < gl_st.min_columns_and_dozens:
                    return {"status": "err","min_val":gl_st.min_columns_and_dozens}
            elif rule_type == 6:
                if how_many_in_row < gl_st.min_sectors_3:
                    return {"status": "err","min_val":gl_st.min_sectors_3}
            elif rule_type == 7:
                if how_many_in_row < gl_st.min_sectors_6:
                    return {"status": "err","min_val":gl_st.min_sectors_6}
            elif rule_type == 8:
                if how_many_in_row < gl_st.min_sectors:
                    return {"status": "err","min_val":gl_st.min_sectors}
            elif rule_type == 9:
                if how_many_in_row < gl_st.min_alts:
                    return {"status": "err","min_val":gl_st.min_alts}
            elif rule_type == 10:
                if how_many_in_row < gl_st.min_numbers:
                    return {"status": "err","min_val":gl_st.min_numbers}
            elif rule_type == 11:
                if how_many_in_row < 30:
                    return {"status": "err","min_val":30}
            rule.is_tg_on = True
        else:
            rule.is_tg_on = False
            TlgMsg.objects.filter(rule=rule).delete()
        rule.save()
        return {"status": "ok"}

def change_fav_num(usr, num):
    """Добаляет/убирает число num в/из любимых"""
    checked_nums = usr.usersetting.checked_nums
    if num in checked_nums:
        checked_nums.remove(num)
    else:
        checked_nums.append(num)
    usr.usersetting.checked_nums = checked_nums
    usr.usersetting.save()
    return {"status":"ok"}