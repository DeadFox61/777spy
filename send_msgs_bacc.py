import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roulette.settings")
import django
django.setup()
import time
from main.models import TlgMsgBacc



def send_all_msgs():
    msgs = TlgMsgBacc.objects.filter(is_stoped=True)
    for msg in msgs:
        msg.stop_msg()
    msgs = TlgMsgBacc.objects.filter(is_sended=False)
    for msg in msgs:
        msg.send_or_edit()

while True:
    try:
        send_all_msgs()
        time.sleep(0.5)
    except Exception as e:
        print(e)