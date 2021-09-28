import telebot
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.db.models.functions import Greatest
from django.core.validators import MinValueValidator, MaxValueValidator

from . import langs

# Create your models here.

NUM_RED = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

ZERO_SEC = [0, 3, 12, 15, 26, 32, 35]
ORPHELINS_SEC = [1, 6, 9, 14, 17, 20, 31, 34]
TIERS_SEC = [5, 8, 10, 11, 13, 16, 23, 24, 27, 30, 33, 36]
VOISINS_SEC = [2, 4, 7, 18, 19, 21, 22, 25, 28, 29]
ANGLES_SECS = [
    [0, 1, 2], [0, 2, 3],
    [1, 2, 4, 5], [2, 3, 5, 6], [4, 5, 7, 8], [5, 6, 8, 9],
    [7, 8, 10, 11], [8, 9, 11, 12],
    [10, 11, 13, 14], [11, 12, 14, 15], [13, 14, 16, 17], [14, 15, 17, 18],
    [16, 17, 19, 20], [17, 18, 20, 21], [19, 20, 22, 23], [20, 21, 23, 24],
    [22, 23, 25, 26], [23, 24, 26, 27], [25, 26, 28, 29], [26, 27, 29, 30],
    [28, 29, 31, 32], [29, 30, 32, 33], [31, 32, 34, 35], [32, 33, 35, 36]
]

class Baccarat(models.Model):
    name = models.CharField(max_length=50)
    bacc_id = models.CharField(max_length=30)
    provider = models.CharField(max_length=30,default = "Evolution")
    stats = models.JSONField(null=True, blank=True)
    game_state = models.CharField(max_length= 120, blank=True)
    sort_id = models.IntegerField()
    def __str__(self):
        return f"({self.sort_id})({self.provider}){self.name}"

class Roulette(models.Model):
    def __str__(self):
        return f"({self.roul_id}){self.name}"
    name = models.CharField(max_length=50)
    roul_id = models.IntegerField()
    new_stats = models.JSONField(null=True, blank=True)
    def get_name(self):
        if self.roul_id>29:
            prod = "Ezugi"
        else:
            prod = "EG"
        return f"{prod} {self.name}"


class Number(models.Model):
    roulette = models.ForeignKey(Roulette, on_delete=models.CASCADE)
    num = models.IntegerField()
    
    def __str__(self):
        return f"({self.roulette.roul_id}){self.num}"

    def is_zero(self):
        return self.num == 0

    def is_red(self):
        return self.num in NUM_RED

    def get_sector(self):
        number = self.num
        if number in ZERO_SEC:
            return "zero"
        elif number in ORPHELINS_SEC:
            return "orphelins"
        elif number in TIERS_SEC:
            return "tiers"
        elif number in VOISINS_SEC:
            return "voisins"

    def is_even(self):
        return self.num % 2 == 0

    def get_sector_3(self):
        return (self.num-1) // 3 + 1

    def get_column(self):
        return (self.num-1) % 3 + 1

    def get_sectors_6(self):
        sect_id = (self.num-1) // 3 + 1
        return [sect_id-1, sect_id]

    def get_dozen(self):
        return (self.num-1) // 12 + 1

    def is_big(self):
        return self.num > 18

    def get_angles(self):
        number = self.num
        angles = []
        for i in range(len(ANGLES_SECS)):
            if number in ANGLES_SECS[i]:
                angles.append(i+1)
        return angles




class TlgBot(models.Model):
    tg_token = models.CharField(max_length=60)
    name = models.CharField(max_length=20)

    def send_msg(self, user, msg):
        if not user.tlg_id:
            return -1
        bot = telebot.TeleBot(self.tg_token, threaded=False)
        return bot.send_message(user.tlg_id, msg)

    def edit_msg(self, user, msg, msg_id):
        if not user.tlg_id:
            return -1
        bot = telebot.TeleBot(self.tg_token, threaded=False)
        try:
            return bot.edit_message_text(msg, user.tlg_id, msg_id)
        except Exception as e:
            pass
            # print(e)

    def __str__(self):
        return f"{self.name} bot"



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('pro_time', timezone.now())
        account = self.model(login=self.normalize_email(email), **extra_fields)
        account.set_password(password)
        account.usersetting = UserSetting()
        account.save()
        account.usersetting.save()
        return account

    def create_superuser(self, login, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(login, password, **extra_fields)


class User(AbstractBaseUser):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_partner = models.BooleanField(default=False)

    referrer = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    referrer_link = models.ForeignKey('RefLink', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')

    login = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    usr_telegram = models.CharField(max_length=20, blank=True)
    pro_time = models.DateTimeField()
    tlg_id = models.CharField(max_length=20, blank=True)
    tlg_bot = models.ForeignKey(TlgBot, null=True, blank=True, on_delete=models.SET_NULL)
    online_time_sec = models.IntegerField(default=0)

    USERNAME_FIELD = 'login'
    EMAIL_FIELD = 'login'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @admin.display(description='is pro', boolean = True, ordering='pro_time')
    def get_is_pro(self):
        return self.pro_time > timezone.now()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_bot(self):
        if not self.tlg_bot:
            tg_bots = TlgBot.objects.all()
            min_count = 10000000
            min_bot = None
            for tg_bot in tg_bots:
                if tg_bot.user_set.count() < min_count:
                    min_count = tg_bot.user_set.count()
                    min_bot = tg_bot
            self.tlg_bot = min_bot
            self.save()
        return self.tlg_bot



class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curr_roulettes = models.ManyToManyField(Roulette, null=True, blank=True)
    curr_baccarats = models.ManyToManyField(Baccarat, null=True, blank=True)
    is_zero = models.JSONField(
        default={
            "fifty_fifty": 0,
            "dozen_column": 0,
            "alt_fifty_fifty": 0,
            "alt_dozen_column": 0
        }
    )
    checked_nums = models.JSONField(default=[], blank=True)
    show_nums_count = models.IntegerField(default=100)
    individual_stats = models.JSONField(default={}, blank=True)

    def __str__(self):
        return f"{self.user.login} settings"

class PartnerSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance_current = models.IntegerField(default=0)
    balance_wait = models.IntegerField(default=0)
    balance_paid = models.IntegerField(default=0)
    percent = models.IntegerField(default=25 ,validators=[
        MinValueValidator(0),
        MaxValueValidator(100)])
    curr_promo = models.ManyToManyField('Promo', null=True, blank=True)
    def get_clicks_count(self):
        reflinks = self.user.reflink_set.all()
        count = 0
        for reflink in reflinks:
            count += reflink.get_clicks_count()
        return count

    def get_reg_count(self):
        reflinks = self.user.reflink_set.all()
        count = 0
        for reflink in reflinks:
            count += reflink.get_reg_count()
        return count


class Promo(models.Model):
    value = models.CharField(max_length=255, unique=True)
    free_days = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.value}"

class RefLink(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, unique=True)
    promo = models.ForeignKey(Promo, null=True, blank=True, on_delete=models.SET_NULL)
    source = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    def get_clicks_count(self):
        return self.clickentry_set.count()
    def get_reg_count(self):
        return self.referrals.count()
    def __str__(self):
        return f"{self.value} link of {self.user.login}"

class ClickEntry(models.Model):
    link = models.ForeignKey(RefLink, on_delete=models.CASCADE)
    ip = models.CharField(max_length=25, unique=True)
    def __str__(self):
        return f"{self.ip} click of {self.link}"

class Pay(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    data = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f'{self.data.strftime("%Y-%m-%d %H:%M:%S")}:{self.user.login} pay {self.amount} rub'

class Rule(models.Model):
    name = models.CharField(max_length=50)
    is_in_row = models.BooleanField()
    rule_type = models.IntegerField()
    how_many_in_row = models.IntegerField()
    max_count = models.IntegerField(default=9999)
    color = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_tg_on = models.BooleanField(default=False)

    def get_category(self):
        if self.rule_type > 100:
            return 1
        else:
            return 0

    def get_text_info(self, lg="ru"):
        lang = langs.en if lg == "en" else langs.ru
        name = self.name

        category = self.get_category()
        if category == 1:
            category = "Другое"
        else:
            if self.is_in_row:
                category = lang["func"]["menu"]["2"]  # выпало
            else:
                category = lang["func"]["menu"]["1"]  # не выпало

        if (self.rule_type == 1):
            rule_type = 'Red/Black'
        elif (self.rule_type == 2):
            rule_type = 'Even/Odd'
        elif (self.rule_type == 3):
            rule_type = 'Low/High'
        elif (self.rule_type == 4):
            rule_type = lang["func"]["menu"]["6"]  # дюжины
        elif (self.rule_type == 5):
            rule_type = lang["func"]["menu"]["7"]  # колонки
        elif (self.rule_type == 6):
            rule_type = lang["func"]["menu"]["8"]  # сектора по 3
        elif (self.rule_type == 7):
            rule_type = lang["func"]["menu"]["9"]  # Сектора по 6
        elif (self.rule_type == 8):
            rule_type = lang["func"]["menu"]["10"]  # Сектора рулетки
        elif (self.rule_type == 9):
            rule_type = lang["func"]["menu"]["11"]  # череда
        elif (self.rule_type == 10):
            rule_type = lang["func"]["menu"]["12"]  # число
        elif (self.rule_type == 11):
            rule_type = "Череда стритов по 3"
        elif (self.rule_type == 101):
            rule_type = "fav"

        how_many_in_row = self.how_many_in_row

        if (self.color == 1):
            color = "green"  # зеленый
        elif (self.color == 2):
            color = "yellow"  # желтый
        elif (self.color == 3):
            color = "red"  # красный
        return {
            "name": name,
            "category": category,
            "rule_type": rule_type,
            "how_many_in_row": how_many_in_row,
            "color": color
        }

    def __str__(self):
        return f"{self.user.login} rule {self.name}"

class BaccRule(models.Model):
    name = models.CharField(max_length=50)
    rule_type = models.IntegerField()
    count = models.IntegerField()
    color = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_tg_on = models.BooleanField(default=False)

    def get_text_info(self, lg="ru"):
        lang = langs.en if lg == "en" else langs.ru
        name = self.name

        if (self.rule_type == 1):
            rule_type = 'Банк'
        elif (self.rule_type == 2):
            rule_type = 'Игрок'
        elif (self.rule_type == 3):
            rule_type = 'Ничья'

        count = self.count

        if (self.color == 1):
            color = "green"  # зеленый
        elif (self.color == 2):
            color = "yellow"  # желтый
        elif (self.color == 3):
            color = "red"  # красный
        return {
            "name": name,
            "rule_type": rule_type,
            "count": count,
            "color": color
        }
    def __str__(self):
        return f"{self.user.login} rule {self.name}"
class TlgMsgBacc(models.Model):
    is_sended = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rule = models.ForeignKey(BaccRule, on_delete=models.CASCADE)

    bacc_name = models.CharField(max_length=40)
    rule_name = models.CharField(max_length=20)
    count = models.IntegerField()
    is_stoped = models.BooleanField(default=False)
    msg_id = models.IntegerField(default=-1)

    def send_or_edit(self):
        edit_msgs = TlgMsgBacc.objects.filter(
            rule = self.rule,
            user=self.user,
            is_sended=True,
            bacc_name=self.bacc_name,
            rule_name=self.rule_name
        )
        if edit_msgs:
            edit_msgs[0].up_msg(self.count)
            self.delete()
        else:
            self.send_msg()
    msg_id = models.IntegerField(default=-1)

    def send_msg(self):
        ordr_text = "не выпало подряд"
        # while True:
        try:
            msg = self.user.get_bot().send_msg(
                self.user,
                f"На {self.bacc_name} {ordr_text} {self.rule_name} в количестве {self.count}"
            )
            # break
            self.msg_id = msg.id
            if msg == -1:
                self.delete()
                return
        except Exception as e:
            # pass
            print(e)
        self.is_sended = True
        self.save()
        
        

    def stop_msg(self):
        ordr_text = "не выпало подряд"
        try:
            self.user.get_bot().edit_msg(
                self.user,
                f"На {self.bacc_name} {ordr_text} {self.rule_name} в количестве {self.count} 🚫",
                self.msg_id
            )
        except Exception as e:
            print(e)
        self.delete()

    def up_msg(self, new_count):
        ordr_text = "не выпало подряд"
        if self.count < new_count:
            self.user.get_bot().edit_msg(
                self.user,
                f"На {self.bacc_name} {ordr_text} {self.rule_name} в количестве {new_count} ⏫",
                self.msg_id
            )
        self.count = new_count
        self.save()

    def __str__(self):
        txt = "stop_msg" if self.is_stoped else "send_msg"
        return f"{self.user.login} {txt}"


class TlgMsg(models.Model):
    is_sended = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)

    roul_name = models.CharField(max_length=40)
    is_in_order = models.BooleanField()
    rule_name = models.CharField(max_length=20)
    count = models.IntegerField()
    is_stoped = models.BooleanField(default=False)

    def send_or_edit(self):
        edit_msgs = TlgMsg.objects.filter(
            rule = self.rule,
            user=self.user,
            is_sended=True,
            roul_name=self.roul_name,
            is_in_order=self.is_in_order,
            rule_name=self.rule_name
        )
        if edit_msgs:
            edit_msgs[0].up_msg(self.count)
            self.delete()
        else:
            self.send_msg()
    msg_id = models.IntegerField(default=-1)

    def send_msg(self):
        ordr_text = "выпало подряд" if self.is_in_order else "не выпало подряд"
        category = self.rule.get_category()
        try:
            if category == 0:
                msg = self.user.get_bot().send_msg(
                    self.user,
                    f"На {self.roul_name} {ordr_text} {self.rule_name} в количестве {self.count}"
                )
            elif category == 1:
                msg = self.user.get_bot().send_msg(
                    self.user,
                    f"На {self.roul_name} значение {self.rule_name} равно {self.count}"
                )
            if msg == -1:
                self.delete()
                return
            self.msg_id = msg.id
        except Exception as e:
            print(e)
        self.is_sended = True
        self.save()
        
        

    def stop_msg(self):
        ordr_text = "выпало подряд" if self.is_in_order else "не выпало подряд"
        category = self.rule.get_category()
        try:
            if category == 0:
                self.user.get_bot().edit_msg(
                    self.user,
                    f"На {self.roul_name} {ordr_text} {self.rule_name} в количестве {self.count} 🚫",
                    self.msg_id
                )
            elif category == 1:
                self.user.get_bot().edit_msg(
                    self.user,
                    f"На {self.roul_name} значение {self.rule_name} равно {self.count} 🚫"
                )
        except Exception as e:
            print(e)
        self.delete()

    def up_msg(self, new_count):
        ordr_text = "выпало подряд" if self.is_in_order else "не выпало подряд"
        category = self.rule.get_category()
        if self.count < new_count:
            icon = "⏫"
        elif self.count > new_count:
            icon = "⏬"
        else:
            return
        try:
            if category == 0:
                self.user.get_bot().edit_msg(
                    self.user,
                    f"На {self.roul_name} {ordr_text} {self.rule_name} в количестве {new_count} {icon}",
                    self.msg_id
                )
            elif category == 1:
                self.user.get_bot().edit_msg(
                    self.user,
                    f"На {self.roul_name} значение {self.rule_name} равно {new_count} {icon}",
                    self.msg_id
                )
        except Exception as e:
            print(e)
        self.count = new_count
        self.save()

    def __str__(self):
        return f"{self.user.login} {self.rule_name}"

class ParseData(models.Model):
    version = models.IntegerField()
    evo_id = models.CharField(max_length=120)
        

class GlobalSetting(models.Model):
    version = models.IntegerField()
    price_day = models.IntegerField(default = 1000)
    price_week = models.IntegerField(default = 5000)
    price_month = models.IntegerField(default = 15000)
    site_msg = models.CharField(max_length=255, blank=True)
    free_rouls_available = models.IntegerField()
    free_rules_available = models.IntegerField()
    min_chances = models.IntegerField()
    min_columns_and_dozens = models.IntegerField()
    min_alts = models.IntegerField()
    min_sectors = models.IntegerField()
    min_sectors_3 = models.IntegerField()
    min_sectors_6 = models.IntegerField()
    min_numbers = models.IntegerField()