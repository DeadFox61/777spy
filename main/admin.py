from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Roulette, Number, UserSetting, Rule, TlgBot, TlgMsg, TlgMsgBacc, GlobalSetting, Baccarat, ParseData, BaccRule

class UserSettingInline(admin.StackedInline):
    model = UserSetting

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('login','phone', 'is_staff','is_pro','usr_telegram', 'online_time_min','pro_time',)

    def online_time_min(self, obj):
        return f"{obj.online_time_sec//60} мин"
    online_time_min.short_description = 'Online time'
    
    list_filter = ('is_pro','is_staff', )
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_pro')}),
        ('Info',{'fields':('phone','usr_telegram','tlg_id','tlg_bot','pro_time')})
    )
    inlines = [UserSettingInline]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('login',)
    ordering = ('-is_staff','-is_pro','login',)
    filter_horizontal = ()
    has_module_perms = None

class RouletteAdmin(admin.ModelAdmin):
    ordering = ('roul_id',)
class BaccaratAdmin(admin.ModelAdmin):
    ordering = ('sort_id',)

class NumberModelAdmin(admin.ModelAdmin):
    list_display = ('roulette', 'num',)
    list_filter = (
        'is_new',
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