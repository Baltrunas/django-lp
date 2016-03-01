# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.utils import timezone

from ..pages.models import Page


class Request(models.Model):
	config = models.ForeignKey('FormConfig', verbose_name=_('Form Config'), blank=True, null=True)
	site = models.ForeignKey(Site, verbose_name=_('Site'), blank=True, null=True)

	name = models.CharField(max_length=128, verbose_name=_('Name'))
	phone = models.CharField(max_length=32, verbose_name=_('Phone'), blank=True, null=True)
	email = models.EmailField(max_length=128, verbose_name=_('E-Mail'), blank=True, null=True)
	comment = models.TextField(verbose_name=_('Comment'), blank=True, null=True)

	ip = models.GenericIPAddressField(blank=True, null=True, editable=False, verbose_name=_('IP'))
	referrer = models.CharField(verbose_name=_('Referrer'), max_length=2048, blank=True, null=True, editable=False)

	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return 'Request #%s from %s' % (self.pk, self.name)

	class Meta:
		ordering = ['-created_at']
		verbose_name = _('Msg')
		verbose_name_plural = _('Msgs')


class FormConfig(models.Model):
	title = models.CharField(max_length=128, verbose_name=_('Title'))
	show_title = models.BooleanField(verbose_name=_('Show form title'), default=False)
	submit_name = models.CharField(max_length=128, verbose_name=_('Submit bottom name'))

	phone = models.BooleanField(verbose_name=_('Show phone field'), default=True)
	phone_placeholder = models.CharField(max_length=128, verbose_name=_('Phone placeholder'), blank=True, null=True)

	email = models.BooleanField(verbose_name=_('Show e-mail field'), default=False)
	email_placeholder = models.CharField(max_length=128, verbose_name=_('E-Mail placeholder'), blank=True, null=True)

	comment = models.BooleanField(verbose_name=_('Show comment field'), default=False)
	comment_placeholder = models.CharField(max_length=128, verbose_name=_('Comment placeholder'), blank=True, null=True)

	error_message = models.TextField(verbose_name=_('Error Message'), blank=True, null=True)
	tnx_message = models.TextField(verbose_name=_('Tnx Message'), blank=True, null=True)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)


	def get_form(self, initial=None):
		exclude_field = ['user', 'site', 'config']
		if not self.phone:
			exclude_field.append('phone')
			phone_field = False
		else:
			phone_field = forms.CharField(label=_('Phone'), max_length=200, widget=forms.TextInput(attrs={'required': 'required', 'placeholder': self.phone_placeholder}), required=True)

		if not self.email:
			exclude_field.append('email')
			email_field = False
		else:
			email_field = forms.EmailField(label=_('E-Mail'), max_length=200, widget=forms.TextInput(attrs={'type': 'email', 'required': 'required', 'placeholder': self.email_placeholder}), required=True)

		if not self.comment:
			exclude_field.append('comment')
			comment_field = False
		else:
			comment_field = forms.CharField(label=_('Comment'), widget=forms.Textarea(attrs={'placeholder': self.comment_placeholder}), required=True)

		config_field = forms.CharField(widget=forms.HiddenInput(), initial=self.id)

		class RequestForm(forms.ModelForm):
			config = config_field
			name = forms.CharField(label=_('Name'), max_length=200, widget=forms.TextInput(attrs={'required': 'required', 'placeholder': _('Name')}))

			if phone_field:
				phone = phone_field

			if email_field:
				email = email_field

			if comment_field:
				comment = comment_field

			class Meta:
				model = Request
				exclude = exclude_field

		return RequestForm(initial)

	@models.permalink
	def get_absolute_url(self):
		return ('request', (), {'id': self.id})

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-created_at']
		verbose_name = _('Form Config')
		verbose_name_plural = _('Forms Configs')


class CountDown(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=128)
	to_datetime = models.DateTimeField(verbose_name=_('To Date Time'))
	repeat = models.PositiveIntegerField(verbose_name=_('Repeat each in hours'), default=0, blank=True, null=True)
	img = models.ImageField(verbose_name=_('Image'), upload_to='img/countdown', default=0, blank=True, null=True)
	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return self.name

	def is_active(self):
		if self.to_datetime < timezone.now():
			return True

		if self.repeat:
			self.to_datetime += datetime.timedelta(hours=self.repeat)
			self.save()
			return True

		return False

	class Meta:
		ordering = ['updated_at', 'name', 'to_datetime']
		verbose_name = _('Count Down')
		verbose_name_plural = _('Count Downs')


class SiteConfig(models.Model):
	# TODO: sites?
	site = models.ForeignKey(Site, verbose_name=_('Site'), related_name='config')

	title = models.CharField(verbose_name=_('Title'), max_length=128)

	send_sms = models.BooleanField(verbose_name=_('Send SMS'), default=True)
	phone = models.CharField(max_length=32, verbose_name=_('Phone'))

	sms_key = models.CharField(verbose_name=_('SMS.RU Key'), max_length=64, blank=True, null=True)

	sms_name = models.CharField(verbose_name=_('SMS Name'), help_text=_('From 2 to 11 Latin characters. As senders, we endorse only the names of sites, organizations or brands.'), max_length=11)

	send_email = models.BooleanField(verbose_name=_('Send E-Mail'), default=True)
	email = models.EmailField(max_length=128, verbose_name=_('E-Mail'))

	code_head = models.TextField(verbose_name=_('Head Code'), blank=True, null=True)
	code_footer = models.TextField(verbose_name=_('Footer Code'), blank=True, null=True)

	form_config = models.ForeignKey(FormConfig, verbose_name=_('Pop-Up Form (CallBack)'), blank=True, null=True)

	VALUTE_CHOICES = (
		('rub', u'Р.'),
		('usd', u'$'),
		('eur', u'€'),
	)
	valute = models.CharField(verbose_name=_('Valute'), max_length=3, choices=VALUTE_CHOICES)

	favicon = models.FileField(verbose_name=_('Favicon'), upload_to='conf/img', blank=True, null=True)
	logo = models.FileField(verbose_name=_('Logo'), upload_to='conf/img', blank=True, null=True)
	logo_small = models.FileField(verbose_name=_('Logo Small'), upload_to='conf/img', blank=True, null=True)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return u'%s &rarr; %s' % (self.site, self.title)
	__unicode__.allow_tags = True

	class Meta:
		verbose_name = _('Site Config')
		verbose_name_plural = _('Sites Config')


class Block(models.Model):
	title = models.CharField(verbose_name=_('Title'), max_length=256)
	hide_title = models.BooleanField(verbose_name=_('Hide Title'), default=False)
	slug = models.SlugField(verbose_name=_('Slug'), max_length=128)
	sub_title = models.CharField(verbose_name=_('Sub Title'), max_length=256, blank=True, null=True)
	text = models.TextField(verbose_name=_('Text'), blank=True, null=True)
	image = models.FileField(verbose_name=_('Image'), upload_to='block/image', blank=True, null=True)
	bg = models.FileField(verbose_name=_('Background'), upload_to='block/bg', blank=True, null=True)

	# template = models.CharField(_('Template'), max_length=124, blank=True, null=True)

	pages = models.ManyToManyField(Page, related_name='blocks', verbose_name=_('Sites'), blank=True)
	order = models.PositiveSmallIntegerField(verbose_name=_('Sort'), default=500)

	form_config = models.ForeignKey(FormConfig, verbose_name=_('Form Config'), blank=True, null=True)

	offices = models.BooleanField(verbose_name=_('Offices'), default=False)


	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def public_reviews(self):
		return self.reviews.filter(public=True)

	def public_subblocks(self):
		return self.subblocks.filter(public=True)

	def public_tariffs(self):
		return self.tariffs.filter(public=True)

	def public_tariffs_options(self):
		options = []
		for tariff in self.public_tariffs():
			for option in tariff.options_list():
				options.append(option)
		return set(options)

	def public_tariffs_properties(self):
		properties = []
		for tariff in self.public_tariffs():
			for propert in tariff.property_list():
				properties.append(propert)
		return set(properties)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['order']
		verbose_name = _('Block')
		verbose_name_plural = _('Blocks')


class SubBlock(models.Model):
	title = models.CharField(verbose_name=_('Title'), max_length=256)
	block = models.ForeignKey(Block, verbose_name=_('Block'), related_name='subblocks')
	sub_title = models.CharField(verbose_name=_('Sub Title'), max_length=256, blank=True, null=True)
	description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
	image = models.FileField(verbose_name=_('Image'), upload_to='subblock/image', blank=True, null=True)

	order = models.PositiveSmallIntegerField(verbose_name=_('Sort'), default=500)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['block', 'order']
		verbose_name = _('Sub Block')
		verbose_name_plural = _('Sub Blocks')


class FAQ(models.Model):
	block = models.ForeignKey(Block, verbose_name=_('Block'), related_name='faqs')

	problem_title = models.CharField(verbose_name=_('Problem Title'), max_length=256)
	problem_description = models.TextField(verbose_name=_('Problem Description'), blank=True, null=True)
	problem_image = models.FileField(verbose_name=_('Problem Image'), upload_to='faq/image', blank=True, null=True)

	solutions_title = models.CharField(verbose_name=_('Solutions Title'), max_length=256)
	solutions_description = models.TextField(verbose_name=_('Solutions Description'), blank=True, null=True)
	solutions_image = models.FileField(verbose_name=_('Solutions Image'), upload_to='faq/image', blank=True, null=True)

	order = models.PositiveSmallIntegerField(verbose_name=_('Sort'), default=500)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return self.problem_title

	class Meta:
		ordering = ['order']
		verbose_name = _('FAQ')
		verbose_name_plural = _('FAQs')


class TariffAddition(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=256)
	description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
	price = models.PositiveIntegerField(verbose_name=_('Price'), default=1000, null=True, blank=True)

	price_from = models.BooleanField(verbose_name=_('Price From'), default=False)
	price_after = models.CharField(verbose_name=_('Price After'), max_length=256, blank=True, null=True)

	selected = models.BooleanField(verbose_name=_('Selected'), default=True)
	order = models.PositiveSmallIntegerField(verbose_name=_('Sort'), default=500)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['order']
		verbose_name = _('Tariff Addition')
		verbose_name_plural = _('Tariffs Additions')


class Tariff(models.Model):
	block = models.ForeignKey(Block, verbose_name=_('Block'), related_name='tariffs')

	title = models.CharField(verbose_name=_('Title'), max_length=256)
	sub_title = models.CharField(verbose_name=_('Sub Title'), max_length=256)

	old_price = models.PositiveIntegerField(verbose_name=_('Old Price'), default=1000, null=True, blank=True)
	new_price = models.PositiveIntegerField(verbose_name=_('New Price'), default=1000, null=True, blank=True)

	price_from = models.BooleanField(verbose_name=_('Price From'), default=False)
	price_after = models.CharField(verbose_name=_('Price After'), max_length=256, blank=True, null=True)

	description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
	options = models.TextField(verbose_name=_('Options'), blank=True, null=True)

	image = models.FileField(verbose_name=_('Image'), upload_to='tariff/image', blank=True, null=True)

	order_url = models.URLField(verbose_name=_('Order URL'), max_length=256, blank=True, null=True)

	order = models.PositiveSmallIntegerField(verbose_name=_('Sort'), default=500)

	additions = models.ManyToManyField(TariffAddition, verbose_name=_('Additions'), blank=True, related_name='tariff')

	vip = models.BooleanField(verbose_name=_('VIP'), default=True)
	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def options_list(self):
		options_list = []
		for option in self.options.split("\n"):
			if len(option.split(": ")) < 2:
				options_list.append(option.strip())
		return options_list

	def property_list(self):
		property_list = []
		for option in self.options.split("\n"):
			property_value = option.split(": ")
			if len(property_value) > 1:
				property_list.append(property_value[0].strip())
		return property_list

	def get_property_value(self, propert):
		for option in self.options.split("\n"):
			property_value = option.split(": ")
			if len(property_value) > 1:
				if property_value[0].strip() == propert:
					return property_value[1].strip()

	def public_additions(self):
		return self.additions.filter(public=True)

	@models.permalink
	def url(self):
		return ('tariff', (), {'id': self.id})

	def get_absolute_url(self):
		if self.order_url:
			return self.order_url
		else:
			return self.url()

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['order']
		verbose_name = _('Tariff')
		verbose_name_plural = _('Tariffs')


class TariffOrder(models.Model):
	site = models.ForeignKey(Site, verbose_name=_('Site'), blank=True, null=True)

	name = models.CharField(max_length=128, verbose_name=_('Name'), help_text=_('Gleb'))
	phone = models.CharField(max_length=32, verbose_name=_('Phone'), help_text=_('+7 (965) 222-03-30'))
	email = models.EmailField(max_length=128, verbose_name=_('E-Mail'), help_text=_('gleb@gmail.com'))

	ip = models.GenericIPAddressField(blank=True, null=True, editable=False, verbose_name=_('IP'))
	referrer = models.CharField(verbose_name=_('Referrer'), max_length=2048, blank=True, null=True, editable=False)

	tariff = models.ForeignKey(Tariff, verbose_name=_('Tariff'), null=True)
	additions = models.ManyToManyField(TariffAddition, verbose_name=_('Additions'), blank=True)

	total_price = models.PositiveIntegerField(verbose_name=_('Total Price'), null=True, blank=True)

	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return '#%s from %s' % (self.pk, self.name)

	class Meta:
		ordering = ['-created_at']
		verbose_name = _('Tariff Order')
		verbose_name_plural = _('Tariff Orders')


# Contacts
class Office(models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=128)

	description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
	orgdata = models.TextField(verbose_name=_('Organization Data'), blank=True, null=True)

	phone = models.CharField(verbose_name=_('Phone'), max_length=64, default='+7 (000) 000-00-00', blank=True, null=True)
	email = models.CharField(verbose_name=_('E-mail'), max_length=128, default='email@mail.com', blank=True, null=True)
	skype = models.CharField(verbose_name=_('Skype'), max_length=128, blank=True)
	address = models.CharField(verbose_name=_('Address'), max_length=2048, blank=True)

	www = models.URLField(verbose_name=_('WWW'), max_length=64, default='http://glav.it/', blank=True, null=True)

	photo = models.ImageField(verbose_name=_('Photo'), upload_to='img/office', blank=True)

	sites = models.ManyToManyField(Site, related_name='offices', verbose_name=_('Sites'))

	latitude = models.DecimalField(verbose_name=_('Latitude'), max_digits=19, decimal_places=15, blank=True, null=True)
	longitude = models.DecimalField(verbose_name=_('Longitude'), max_digits=19, decimal_places=15, blank=True, null=True)

	center_latitude = models.DecimalField(verbose_name=_('Center Latitude'), max_digits=19, decimal_places=15, blank=True, null=True)
	center_longitude = models.DecimalField(verbose_name=_('Center Longitude'), max_digits=19, decimal_places=15, blank=True, null=True)

	zoom = models.PositiveSmallIntegerField(verbose_name=_('Zoom'), default=15)
	order = models.PositiveSmallIntegerField(verbose_name=_('Sort'), default=500)
	main = models.BooleanField(verbose_name=_('Main'), default=True)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def get_latitude(self):
		return '%s' % self.latitude

	def get_longitude(self):
		return '%s' % self.longitude

	def get_center_latitude(self):
		return '%s' % self.center_latitude

	def get_center_longitude(self):
		return '%s' % self.center_longitude

	def phones(self):
		return [phone.strip() for phone in self.phone.split(', ')]

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['order', 'name']
		verbose_name = _('Office')
		verbose_name_plural = _('Offices')
