import re

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render

from django.views import generic
from django.views.decorators.gzip import gzip_page

from . import langs
from .models import Roulette, Rule, User, UserSetting, TlgMsg, TlgMsgBacc, GlobalSetting, Baccarat, BaccRule
from . import site_auth, roulette_api, baccarat_api, contexts, partner_api


def index(request):
    if 'refid' in request.GET:
        response = HttpResponseRedirect('/')
        site_auth.add_click(request.GET['refid'], request.META.get('HTTP_X_REAL_IP'))
        response.set_cookie('refid', request.GET['refid'])
        return response
    if request.user.is_authenticated:
        context = contexts.get_main_page_context(request.user)
        return render(request, 'index.html', context)
    else:
        context = {'text': langs.ru}
        return render(request, 'login.html', context)

def pro(request):
    return render(request, 'pro.html', contexts.get_pro_page_context(request.user))

def partner(request):
    if request.user.is_authenticated and request.user.is_partner:
        context = contexts.get_partner_page_context(request.user)
        return render(request, 'partner.html', context)
    else: 
        raise Http404()

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
        # Логин
        if request.POST['button'] == "1":
            user = authenticate(request, login=user_login, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("1_ok")
            else:
                return HttpResponse("1_no")
        # Регистрация
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

            refid = request.COOKIES.get('refid')
            site_auth.sign_up(
                user_login,
                password,
                phone=signin_phone,
                usr_telegram=signin_telegram,
                refid = refid
            )
            user = authenticate(request, login=user_login, password=password)
            login(request, user)
            return HttpResponse("2_ok")
    elif request.POST['type'] == 'quit':
        logout(request)
        return JsonResponse({'status':'ok'})

    return HttpResponse("aga")


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



# ajax - view рулеток

@gzip_page
def get_stats(request):
    if request.user.is_anonymous:
        return HttpResponse("anon")
    else:
        return JsonResponse(roulette_api.get_stats(request.user))
    
def get_choice_roul(request):
    return JsonResponse(roulette_api.get_choosen(request.user))

def change_roul(request):
    change_roul_id = request.POST['param']
    return JsonResponse(roulette_api.change_choise(request.user,change_roul_id))

def get_zeros(request):
    return JsonResponse(roulette_api.get_zeros(request.user))

def change_zero(request):
    zr_name = request.POST['name']
    return JsonResponse(roulette_api.change_zero(request.user,zr_name))

def add_rule(request):
    usr = request.user
    name = request.POST['name']
    is_in_row = bool(int(request.POST['tables']))
    rule_type = int(request.POST['col'])
    count = int(request.POST['count'])
    color = int(request.POST['color'])
    return JsonResponse(roulette_api.add_rule(usr,name,rule_type,count,color))

def get_rules(request):
    return JsonResponse(roulette_api.get_rules(request.user))

def del_rule(request):
    rule_id = int(request.POST['id'])
    return JsonResponse(roulette_api.del_rule(rule_id))

def get_rule(request):
    rule_id = int(request.POST['id'])
    return JsonResponse(roulette_api.get_rule(rule_id))

def change_tg(request):
    usr = request.user
    rule_id = int(request.POST['id'])
    is_on = bool(int(request.POST['param']))
    return JsonResponse(roulette_api.change_tg(usr,rule_id,is_on))

def change_fav_num(request):
    usr = request.user
    num = int(request.POST['num'])
    return JsonResponse(roulette_api.change_fav_num(usr,num))

# ajax-ы баккарат
def get_stats_bacc(request):
    if request.user.is_anonymous:
        return HttpResponse("anon")
    return JsonResponse(baccarat_api.get_stats(request.user))

def get_choice_bacc(request):
    return JsonResponse(baccarat_api.get_choosen(request.user))

def change_bacc(request):
    change_bacc_id = request.POST['param']
    return JsonResponse(baccarat_api.change_choise(request.user,change_bacc_id))

def add_rule_bacc(request):
    usr = request.user
    name = request.POST['name']
    rule_type = int(request.POST['tables'])
    count = int(request.POST['count'])
    color = int(request.POST['color'])   
    return JsonResponse(baccarat_api.add_rule(usr,name,rule_type,count,color))

def get_rules_bacc(request):
    return JsonResponse(baccarat_api.get_rules(request.user))

def del_rule_bacc(request):
    rule_id = int(request.POST['id'])
    return JsonResponse(baccarat_api.del_rule(rule_id))

def get_rule_bacc(request):
    rule_id = int(request.POST['id'])
    return JsonResponse(baccarat_api.get_rule(rule_id))

def change_tg_bacc(request):
    usr = request.user
    rule_id = int(request.POST['id'])
    is_on = bool(int(request.POST['param']))
    return JsonResponse(baccarat_api.change_tg(usr,rule_id,is_on))


def partner_ajax(request):
    ajax_type = request.POST['type']
    if ajax_type == 'add_new_ref_link':
        return JsonResponse(partner_api.add_new_ref_link(request.user))
    elif ajax_type == 'del_ref_link':
        value = request.POST['value']
        return JsonResponse(partner_api.del_ref_link(request.user, value))
    elif ajax_type == 'partner_ref_edit_save':
        ref_value = request.POST['ref_value']
        promo_value = request.POST['promo_value']
        source = request.POST['source']
        comment = request.POST['comment']
        return JsonResponse(partner_api.partner_ref_edit_save(request.user, ref_value, promo_value, source, comment))
    return JsonResponse({'status':'invalid_type'})