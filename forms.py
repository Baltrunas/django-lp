# -*- coding: utf-8 -*-
from django import forms

from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from apps.seo.models import SiteSettings

from .models import Request
from .models import TariffOrder
from .models import SiteConfig


class Html5EmailInput(forms.widgets.Input):
	input_type = 'email'


class RequestForm(forms.ModelForm):
	class Meta:
		model = Request


class TariffOrderForm(forms.ModelForm):
	name = forms.CharField(label=_('Name'),max_length=200, widget=forms.TextInput(attrs={'required': 'required', 'placeholder': _('Name')}))
	phone = forms.CharField(label=_('Phone'), max_length=200, widget=forms.TextInput(attrs={'required': 'required', 'placeholder': _('Phone')}))
	email = forms.EmailField(label=_('E-Mail'), max_length=200, widget=Html5EmailInput(attrs={'required': 'required', 'placeholder': _('info@express-page.ru')}))

	class Meta:
		model = TariffOrder
		exclude = ['user', 'site', 'tariff', 'total_price']


class SiteConfigForm(forms.ModelForm):
	class Meta:
		model = SiteConfig
		exclude = ['site', 'user']


class SiteForm(forms.ModelForm):
	class Meta:
		model = Site

	def clean_domain(self):
		domain = self.cleaned_data['domain']
		if self.instance.domain:
			if Site.objects.filter(domain=domain).count() > 1:
				raise forms.ValidationError(_('Domain Already Exists'))
		else:
			if Site.objects.filter(domain=domain):
				raise forms.ValidationError(_('Domain Already Exists'))
		return domain


class SiteSettingsForm(forms.ModelForm):
	class Meta:
		model = SiteSettings
		exclude = ['site']
