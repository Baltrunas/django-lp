# -*- coding: utf-8 -*-
import json

import urllib
import urllib2


from django.http import HttpResponse

from django.shortcuts import render

from django.template.loader import render_to_string
from django.template import RequestContext

# from django.utils.translation import ugettext_lazy as _

from django import forms

from django.core.mail import EmailMultiAlternatives
# from django.core.mail import EmailMessage


from .forms import TariffOrderForm

from .models import Office
from .models import SiteConfig
from .models import Tariff
from .models import FormConfig


def urlencode(string):
	string = urllib.unquote(string)
	string = u'' + urllib.quote(string.encode('utf-8'))
	return string


def request(request, id):
	context = {}

	site_config = SiteConfig.objects.get(site=request.site)
	phone = site_config.phone

	config = FormConfig.objects.get(id=id)

	form = config.get_form(request.POST or None)

	if request.POST:
		if form.is_valid():
			new_request = form.save()
			new_request.referrer = request.META.get('HTTP_REFERER', None)
			new_request.ip = request.META.get('REMOTE_ADDR', None)
			new_request.site = request.site
			new_request.config = config
			new_request.save()

			try:
				if site_config.send_sms and site_config.sms_key:
					text = u'Новая заявка!\n%s\n%s\n%s\n%s' % (new_request.name, new_request.phone, new_request.email, new_request.referrer)
					if site_config.sms_name:
						url = 'http://sms.ru/sms/send?api_id=%s&to=%s&text=%s&from=%s&translit=0' % (site_config.sms_key, urlencode(phone), urlencode(text), urlencode(site_config.sms_name))
					else:
						url = 'http://sms.ru/sms/send?api_id=%s&to=%s&text=%s&translit=0' % (site_config.sms_key, urlencode(phone), urlencode(text))
					urllib2.urlopen(url)
			except:
				pass

			if site_config.send_email:
				try:
					email_context = {}
					email_context['title'] = config.title
					email_context['offices'] = Office.objects.filter(public=True, sites__in=[request.site])
					email_context['object'] = new_request
					admin_content = render_to_string('email/result.html', email_context, context_instance=RequestContext(request))
					sendmsg = EmailMultiAlternatives(email_context['title'], admin_content, site_config.email, [site_config.email])
					sendmsg.attach_alternative(admin_content, "text/html")
					sendmsg.send()
				except:
					pass


			context['send'] = True
		else:
			context['errors'] = form.errors
			context['send'] = False

		return HttpResponse(json.dumps(context), content_type="application/json")

	else:
		context['config'] = config
		context['form'] = form
		return render(request, 'lp/page_form.html', context)


def tariff_order(request, id):
	context = {}

	tariff = Tariff.objects.get(id=id)
	site_config = SiteConfig.objects.get(site=request.site)
	context['offices'] = Office.objects.filter(public=True, sites__in=[request.site])
	context['form'] = TariffOrderForm(request.POST or None)
	context['tariff'] = tariff
	context['additions'] = tariff.public_additions()

	context['form'].fields['additions'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=context['additions'], required=False)

	if context['form'].is_valid():
		new_order = context['form'].save()
		new_order.tariff = tariff
		new_order.site = request.site
		new_order.referrer = request.META.get('HTTP_REFERER', None)
		new_order.ip = request.META.get('REMOTE_ADDR', None)
		new_order.total_price = tariff.new_price
		for addition in new_order.additions.all():
			new_order.total_price += addition.price
		new_order.save()

		context['new_order'] = new_order

		# Send admin E-Mail
		# try:
		admin_content = render_to_string('email/tariff_order.html', context, context_instance=RequestContext(request))
		sendmsg = EmailMultiAlternatives(tariff.title, admin_content, site_config.email, [site_config.email])
		sendmsg.attach_alternative(admin_content, "text/html")
		sendmsg.send()


		# except:
		# 	pass

		context['ok'] = True

	return render(request, 'lp/tariff_order.html', context)
