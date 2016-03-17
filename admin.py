from django.contrib import admin

from .models import Block, SubBlock, FAQ


class SubBlockInline(admin.StackedInline):
	model = SubBlock
	extra = 0

class FAQInline(admin.StackedInline):
	model = FAQ
	extra = 0

class BlockAdmin(admin.ModelAdmin): 
	list_display = ['title', 'slug', 'order', 'public']
	search_fields = ['title', 'slug', 'order', 'public']
	list_filter = ['public', 'pages']
	list_editable = ['public', 'order']
	inlines = [SubBlockInline, FAQInline]

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
