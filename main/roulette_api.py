from .models import Roulette, Rule 

def get_stats(user):
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