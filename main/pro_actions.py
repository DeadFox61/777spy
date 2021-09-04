from django.utils import timezone
from datetime import timedelta

def add_pro_days(usr, days=30):
	if days <= 0:
		return
	if usr.pro_time < timezone.now():
		usr.pro_time = timezone.now()
	usr.pro_time += timedelta(days=days)
	usr.save()
