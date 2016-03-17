# -*- coding: utf-8 -*
from django.contrib import admin

from .models import SiteConfig

from .models import Block
from .models import SubBlock
from .models import FAQ

from .models import Tariff
from .models import TariffAddition
from .models import TariffOrder

from .models import FormConfig
from .models import Request

from .models import CountDown


class FormConfigAdmin(admin.ModelAdmin):
	list_display = ['title', 'phone', 'email']
	search_fields = ['title', 'phone', 'email']
	list_filter = ['title', 'phone', 'email']

admin.site.register(FormConfig, FormConfigAdmin)


class RequestAdmin(admin.ModelAdmin):
	list_display = ['name', 'config', 'phone', 'email', 'ip', 'referrer', 'created_at', 'updated_at']
	search_fields = ['name', 'phone', 'email', 'ip', 'referrer', 'created_at', 'updated_at']
	list_filter = ['phone', 'email', 'ip', 'referrer', 'created_at', 'updated_at']

admin.site.register(Request, RequestAdmin)


class CountDownAdmin(admin.ModelAdmin):
	list_display = ['name', 'to_datetime', 'public', 'created_at', 'updated_at']
	search_fields = ['name', 'to_datetime', 'public', 'created_at', 'updated_at']
	list_filter = ['to_datetime', 'public', 'created_at', 'updated_at']
	list_editable = ['to_datetime', 'public']

admin.site.register(CountDown, CountDownAdmin)


class SiteConfigAdmin(admin.ModelAdmin): 
	list_display = ['site', 'title', 'send_sms', 'phone', 'send_email', 'email', 'public']
	search_fields = ['site','title', 'send_sms', 'phone', 'send_email', 'email', 'public']
	list_filter = ['public', 'site', 'send_email', 'send_sms']
	list_editable = ['public', 'send_email', 'send_sms']

admin.site.register(SiteConfig, SiteConfigAdmin)


class SubBlockInline(admin.StackedInline):
	model = SubBlock
	extra = 0

class FAQInline(admin.StackedInline):
	model = FAQ
	extra = 0

class TariffInline(admin.StackedInline):
	model = Tariff
	extra = 0

class BlockAdmin(admin.ModelAdmin): 
	list_display = ['title', 'slug', 'order', 'public']
	search_fields = ['title', 'slug', 'order', 'public']
	list_filter = ['public', 'pages']
	list_editable = ['public', 'order']
	inlines = [SubBlockInline, FAQInline, TariffInline]

admin.site.register(Block, BlockAdmin)


class SubBlockAdmin(admin.ModelAdmin): 
	list_display = ['title', 'block', 'sub_title', 'order', 'public']
	search_fields = ['title', 'block', 'sub_title', 'order', 'public']
	list_filter = ['public']
	list_editable = ['public', 'order']

admin.site.register(SubBlock, SubBlockAdmin)


class FAQAdmin(admin.ModelAdmin): 
	list_display = ['problem_title', 'solutions_title', 'order', 'public']
	search_fields = ['problem_title', 'solutions_title', 'order', 'public']
	list_filter = ['public']
	list_editable = ['public', 'order']

admin.site.register(FAQ, FAQAdmin)


class TariffAdmin(admin.ModelAdmin): 
	list_display = ['title', 'old_price', 'new_price', 'order', 'public']
	search_fields = ['title', 'old_price', 'new_price', 'order', 'public']
	list_filter = ['public']
	list_editable = ['public', 'order']

admin.site.register(Tariff, TariffAdmin)


class TariffAdditionAdmin(admin.ModelAdmin): 
	list_display = ['name', 'price', 'order', 'public']
	search_fields = ['name', 'price', 'order', 'public']
	list_filter = ['public']
	list_editable = ['public', 'order']

admin.site.register(TariffAddition, TariffAdditionAdmin)


class TariffOrderAdmin(admin.ModelAdmin): 
	list_display = ['name', 'phone', 'email', 'total_price', 'ip']
	search_fields = ['name', 'phone', 'email', 'total_price', 'ip']
	list_filter = ['name', 'phone', 'email', 'total_price', 'ip']

admin.site.register(TariffOrder, TariffOrderAdmin)
