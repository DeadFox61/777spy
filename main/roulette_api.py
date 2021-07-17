from .models import Roulette, Rule, GlobalSetting

def get_stats(user):
    """Возвращает статистику рулеток"""
    roul_data = []
    roulettes = Roulette.objects.all().order_by("roul_id")
    selected_rouls = list(user.usersetting.curr_roulettes.all())
    is_zero = user.usersetting.is_zero
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
    data = {"user": {"is_pro": usr.is_pro}, "roulettes": []}
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
        if not usr.is_pro and usr.usersetting.curr_roulettes.count() >= gl_st.free_rouls_available:
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