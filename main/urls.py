from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pro', views.pro, name='pro'),
    path('partner', views.partner, name='partner'),
    path('ajax', views.ajax, name='ajax'),
    path('get_stats', views.get_stats, name='get_stats'),
    path('get_choice_roul', views.get_choice_roul, name='get_choice_roul'),
    path('change_roul', views.change_roul, name='change_roul'),
    path('change_zero', views.change_zero, name='change_zero'),
    path('get_zeros', views.get_zeros, name='get_zeros'),
    path('add_rule', views.add_rule, name='add_rule'),
    path('get_rules', views.get_rules, name='get_rules'),
    path('del_rule', views.del_rule, name='del_rule'),
    path('get_clean_rule', views.get_rule, name='get_rule'),
    path('change_tg', views.change_tg, name='change_tg'),
    path('change_tg_bacc', views.change_tg_bacc, name='change_tg_bacc'),
    path('save_tg_id', views.save_tg_id, name='save_tg_id'),
    path('add_sec', views.add_sec, name='add_sec'),
    path('get_choice_bacc', views.get_choice_bacc, name='get_choice_bacc'),
    path('change_bacc', views.change_bacc, name='change_bacc'),
    path('add_rule_bacc', views.add_rule_bacc, name='add_rule_bacc'),
    path('get_rules_bacc', views.get_rules_bacc, name='get_rules_bacc'),
    path('del_rule_bacc', views.del_rule_bacc, name='del_rule_bacc'),
    path('get_clean_rule_bacc', views.get_rule_bacc, name='get_rule_bacc'),
    path('get_stats_bacc', views.get_stats_bacc, name='get_stats_bacc'),
    path('partner_ajax', views.partner_ajax, name='partner_ajax')
]