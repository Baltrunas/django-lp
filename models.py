# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.utils import timezone

from ..pages.models import Page


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
