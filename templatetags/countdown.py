from django import template
register = template.Library()

from ..models import CountDown


@register.simple_tag(takes_context=True)
def countdown(context, id, modifer='eggo'):
	context['countdown'] = CountDown.objects.get(public=True, id=id)
	context['modifer'] = modifer
	tpl = template.loader.get_template('lp/countdown.html')
	return tpl.render(template.Context(context))
