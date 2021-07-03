from .models import Baccarat, BaccRule

def get_stats(user):
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
    