from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry
from django.utils import timezone
from django.db.models import F, Func
from django.db.models.functions import Now

from .models import User, Roulette, Number, UserSetting, Rule, TlgBot, TlgMsg, TlgMsgBacc, GlobalSetting, Baccarat, ParseData, BaccRule, PartnerSetting, Promo, RefLink, ClickEntry, Pay

class UserSettingInline(admin.StackedInline):
    model = UserSetting
class PartnerSettingInline(admin.StackedInline):
    model = PartnerSetting

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('login','phone', 'is_staff','get_is_pro','usr_telegram', 'online_time_min','pro_time_if_pro',)

    @admin.display(description='Online time')
    def online_time_min(self, obj):
        return f"{obj.online_time_sec//60} мин"
    @admin.display()
    def pro_time_if_pro(self,obj):
        if obj.get_is_pro():
            return obj.pro_time
        else:
            return '---'
    search_fields = ('login',)
    ordering = ('-is_staff','login',)
    list_filter = ('is_staff', )

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_partner')}),
        ('Info',{'fields':('phone','usr_telegram','tlg_id','tlg_bot','pro_time','referrer', 'referrer_link')})
    )
    inlines = [UserSettingInline, PartnerSettingInline]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    filter_horizontal = ()
    has_module_perms = None

class RouletteAdmin(admin.ModelAdmin):
    ordering = ('roul_id',)
class BaccaratAdmin(admin.ModelAdmin):
    ordering = ('sort_id',)

class NumberModelAdmin(admin.ModelAdmin):
    list_display = ('roulette', 'num',)
    list_filter = (
        ('roulette', admin.RelatedOnlyFieldListFilter),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserSetting)
admin.site.register(Roulette,RouletteAdmin)
admin.site.register(Rule)
admin.site.register(TlgBot)
admin.site.register(TlgMsg)
admin.site.register(TlgMsgBacc)
admin.site.register(Number,NumberModelAdmin)
admin.site.register(GlobalSetting)
admin.site.register(Baccarat,BaccaratAdmin)
admin.site.register(ParseData)
admin.site.register(BaccRule)
admin.site.register(LogEntry)
admin.site.register(Promo)
admin.site.register(RefLink)
admin.site.register(PartnerSetting)
admin.site.register(ClickEntry)
admin.site.register(Pay)