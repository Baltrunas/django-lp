from django.utils.translation import ugettext as _
from django.db import models

from ..pages.models import Page


class Block(models.Model):
	title = models.CharField(verbose_name=_('Title'), max_length=256)
	hide_title = models.BooleanField(verbose_name=_('Hide Title'), default=False)
	slug = models.SlugField(verbose_name=_('Slug'), max_length=128)
	sub_title = models.CharField(verbose_name=_('Sub Title'), max_length=256, blank=True, null=True)
	text = models.TextField(verbose_name=_('Text'), blank=True, null=True)
	image = models.FileField(verbose_name=_('Image'), upload_to='block/image', blank=True, null=True)
	bg = models.FileField(verbose_name=_('Background'), upload_to='block/bg', blank=True, null=True)

	# template = models.CharField(_('Template'), max_length=124, blank=True, null=True)

	pages = models.ManyToManyField(Page, related_name='blocks', verbose_name=_('Pages'), blank=True)
	order = models.PositiveSmallIntegerField(verbose_name=_('Sort ordering'), default=500)


	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)


	def public_subblocks(self):
		return self.subblocks.filter(public=True)

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

	order = models.PositiveSmallIntegerField(verbose_name=_('Sort ordering'), default=500)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['block', 'order']
		verbose_name = _('Subblock')
		verbose_name_plural = _('Subblocks')


class FAQ(models.Model):
	block = models.ForeignKey(Block, verbose_name=_('Block'), related_name='faqs')

	problem_title = models.CharField(verbose_name=_('Problem Title'), max_length=256)
	problem_description = models.TextField(verbose_name=_('Problem Description'), blank=True, null=True)
	problem_image = models.FileField(verbose_name=_('Problem Image'), upload_to='faq/image', blank=True, null=True)

	solutions_title = models.CharField(verbose_name=_('Solutions Title'), max_length=256)
	solutions_description = models.TextField(verbose_name=_('Solutions Description'), blank=True, null=True)
	solutions_image = models.FileField(verbose_name=_('Solutions Image'), upload_to='faq/image', blank=True, null=True)

	order = models.PositiveSmallIntegerField(verbose_name=_('Sort ordering'), default=500)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return self.problem_title

	class Meta:
		ordering = ['order']
		verbose_name = _('FAQ')
		verbose_name_plural = _('FAQs')
