import re

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.views import generic
from django.views.decorators.gzip import gzip_page

from . import langs
from .models import Roulette, Rule, User, UserSetting, TlgMsg, TlgMsgBacc, GlobalSetting, Baccarat, BaccRule
from . import site_auth, roulette_api, baccarat_api, contexts

def index(request):
    if request.user.is_authenticated:
        context = contexts.get_main_page_context(request.user)
        return render(request, 'index.html', context)
    else:
        context = {'text': langs.ru}
        return render(request, 'login.html', context)

def pro(request):
    return render(request, 'pro.html', {})


# ajax-ы

def ajax(request):
    if request.POST['type'] == 'text':
        return JsonResponse(langs.ru)

    elif request.POST['type'] == 'signin':
        user_login = request.POST['login'].lower()
        password = request.POST['password']
        if not re.match(r"^[a-z0-9\._-]+@[a-z0-9-]+\.[a-z]{2,6}$", user_login):
            return HttpResponse("0_mail")
        if not re.match(r"^([0-9]|[a-z]|[A-Z]){6,}$", password):
            return HttpResponse("0_pass_1")
        if request.POST['button'] == "1":
            user = authenticate(request, login=user_login, password=password)
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                return HttpResponse("1_ok")
            else:
                # No backend authenticated the credentials
                return HttpResponse("1_no")
        elif request.POST['button'] == "2":
            password2 = request.POST['password2']
            if password != password2:
                return HttpResponse("2_pass")
            if User.objects.filter(login=user_login).exists():
                return HttpResponse("2_login")
            signin_phone = request.POST['signin_phone']
            if signin_phone and not re.match(r"^([0-9]|\+){7,20}$", signin_phone):
                return HttpResponse("2_phone")
            signin_telegram = request.POST['signin_telegram']
            if signin_telegram and not re.match(r"^@?([0-9]|[a-z]|[A-Z]){3,}$", signin_telegram):
                return HttpResponse("2_telegram")
            site_auth.sign_up(
                user_login,
                password,
                phone=signin_phone,
                usr_telegram=signin_telegram
            )
            user = authenticate(request, login=user_login, password=password)
            login(request, user)
            return HttpResponse("2_ok")
    return HttpResponse("aga")

def get_stats_bacc(request):
    if request.user.is_anonymous:
        return HttpResponse("anon")
    return JsonResponse(baccarat_api.get_stats(request.user))
    

@gzip_page
def get_stats(request):
    if request.user.is_anonymous:
        return HttpResponse("anon")
    else:
        return JsonResponse(roulette_api.get_stats(request.user))
    


def get_choice_roul(request):
    return JsonResponse(roulette_api.get_choosen(request.user))

def get_choice_bacc(request):
    return JsonResponse(baccarat_api.get_choosen(request.user))


def change_bacc(request):
    change_bacc_id = request.POST['param']
    return JsonResponse(baccarat_api.change_choise(request.user,change_bacc_id))

def change_roul(request):
    change_roul_id = request.POST['param']
    return JsonResponse(roulette_api.change_choise(request.user,change_roul_id))


def get_zeros(request):
    return JsonResponse(roulette_api.get_zeros(request.user))

def change_zero(request):
    zr_name = request.POST['name']
    return JsonResponse(roulette_api.change_zero(request.user,zr_name))

def add_rule_bacc(request):
    usr = request.user
    name = request.POST['name']
    rule_type = int(request.POST['tables'])
    count = int(request.POST['count'])
    color = int(request.POST['color'])   
    return JsonResponse(baccarat_api.add_rule(usr,name,rule_type,count,color))


def add_rule(request):
    usr = request.user
    name = request.POST['name']
    gl_st = GlobalSetting.objects.get(version = 1000)
    is_in_row = bool(int(request.POST['tables']))
    rule_type = int(request.POST['col'])
    how_many_in_row = int(request.POST['count'])
    color = int(request.POST['color'])
    if not usr.is_pro and usr.rule_set.count() >= gl_st.free_rules_available:
        return JsonResponse({"status": "err","min_val":gl_st.free_rules_available})
    rule = Rule(
        name=name,
        is_in_row=is_in_row,
        rule_type=rule_type,
        how_many_in_row=how_many_in_row,
        color=color,
        user=usr
    )
    rule.save()
    return JsonResponse({"status": "ok"})

def get_rules_bacc(request):
    usr = request.user
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
    return JsonResponse({"rules": data_rules})

def get_rules(request):
    usr = request.user
    rules = Rule.objects.filter(user=usr)
    data_rules = []
    for rule in rules:
        rule_text = rule.get_text_info()
        data_rules.append(
            {
                "id": rule.id,
                "name": rule_text["name"],
                "is_in_row": rule_text["is_in_row"],
                "rule_type": rule_text["rule_type"],
                "how_many_in_row": rule_text["how_many_in_row"],
                "color": rule_text["color"],
                "is_tg_on": rule.is_tg_on
            }
        )
    return JsonResponse({"rules": data_rules})

def del_rule_bacc(request):
    rule_id = int(request.POST['id'])
    BaccRule.objects.get(id=rule_id).delete()
    return JsonResponse({"status": "ok"})

def del_rule(request):
    rule_id = int(request.POST['id'])
    Rule.objects.get(id=rule_id).delete()
    return JsonResponse({"status": "ok"})

def get_clean_rule_bacc(request):
    rule_id = int(request.POST['id'])
    rule = BaccRule.objects.get(id=rule_id)
    return JsonResponse(
        {
            "id": rule.id,
            "name": rule.name,
            "rule_type": rule.rule_type,
            "count": rule.count,
            "color": rule.color
        }
    )

def get_clean_rule(request):
    rule_id = int(request.POST['id'])
    rule = Rule.objects.get(id=rule_id)
    return JsonResponse(
        {
            "id": rule.id,
            "name": rule.name,
            "is_in_row": rule.is_in_row,
            "rule_type": rule.rule_type,
            "how_many_in_row": rule.how_many_in_row,
            "color": rule.color
        }
    )

def change_tg_bacc(request):
    usr = request.user
    rule_id = int(request.POST['id'])
    is_on = bool(int(request.POST['param']))
    rule = BaccRule.objects.get(id=rule_id)
    rule_type = rule.rule_type
    count = rule.count
    gl_st = GlobalSetting.objects.get(version = 1000)
    if not usr.is_pro:
        rule.is_tg_on = False
        TlgMsgBacc.objects.filter(rule=rule).delete()
        rule.save()
        return JsonResponse({"status": "err_pro"})
    else:
        if is_on:
            rule.is_tg_on = True
        else:
            rule.is_tg_on = False
            TlgMsgBacc.objects.filter(rule=rule).delete()
        rule.save()
        return JsonResponse({"status": "ok"})

def change_tg(request):
    usr = request.user
    rule_id = int(request.POST['id'])
    is_on = bool(int(request.POST['param']))
    rule = Rule.objects.get(id=rule_id)
    rule_type = rule.rule_type
    how_many_in_row = rule.how_many_in_row
    gl_st = GlobalSetting.objects.get(version = 1000)
    if not usr.is_pro:
        rule.is_tg_on = False
        TlgMsg.objects.filter(rule=rule).delete()
        rule.save()
        return JsonResponse({"status": "err_pro"})
    else:
        if is_on:
            if rule_type == 1 or rule_type == 2 or rule_type == 3:
                if how_many_in_row < gl_st.min_chances:
                    return JsonResponse({"status": "err","min_val":gl_st.min_chances})
            elif rule_type == 4 or rule_type == 5:
                if how_many_in_row < gl_st.min_columns_and_dozens:
                    return JsonResponse({"status": "err","min_val":gl_st.min_columns_and_dozens})
            elif rule_type == 6:
                if how_many_in_row < gl_st.min_sectors_3:
                    return JsonResponse({"status": "err","min_val":gl_st.min_sectors_3})
            elif rule_type == 7:
                if how_many_in_row < gl_st.min_sectors_6:
                    return JsonResponse({"status": "err","min_val":gl_st.min_sectors_6})
            elif rule_type == 8:
                if how_many_in_row < gl_st.min_sectors:
                    return JsonResponse({"status": "err","min_val":gl_st.min_sectors})
            elif rule_type == 9:
                if how_many_in_row < gl_st.min_alts:
                    return JsonResponse({"status": "err","min_val":gl_st.min_alts})
            elif rule_type == 10:
                if how_many_in_row < gl_st.min_numbers:
                    return JsonResponse({"status": "err","min_val":gl_st.min_numbers})
            elif rule_type == 11:
                if how_many_in_row < 30:
                    return JsonResponse({"status": "err","min_val":30})
            rule.is_tg_on = True
        else:
            rule.is_tg_on = False
            TlgMsg.objects.filter(rule=rule).delete()
        rule.save()
        return JsonResponse({"status": "ok"})

def save_tg_id(request):
    tlg_id = request.POST['param']
    usr = request.user
    usr.tlg_id = tlg_id
    usr.save()
    return HttpResponse("yes")

def add_sec(request):
    usr = request.user
    usr.online_time_sec+=1
    usr.save()
    return HttpResponse("ok")
