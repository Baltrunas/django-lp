from django.contrib import admin

from .models import Block, SubBlock


class SubBlockInline(admin.StackedInline):
	model = SubBlock
	extra = 0


class BlockAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'order', 'public']
	search_fields = ['title', 'slug', 'order', 'public']
	list_filter = ['public', 'pages']
	list_editable = ['public', 'order']
	inlines = [SubBlockInline]

admin.site.register(Block, BlockAdmin)


class SubBlockAdmin(admin.ModelAdmin):
	list_display = ['title', 'block', 'sub_title', 'order', 'public']
	search_fields = ['title', 'block', 'sub_title', 'order', 'public']
	list_filter = ['public']
	list_editable = ['public', 'order']

admin.site.register(SubBlock, SubBlockAdmin)
