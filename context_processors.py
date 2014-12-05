from .models import Office


def lp(request):
	context = {}
	try:
		context['offices'] = Office.objects.filter(public=True, sites__in=[request.site])
	except:
		pass
	return context
