from django.utils.translation import ugettext as _
from django.db import models

from helpful.fields import upload_to

from ..pages.models import Page

class Block(models.Model):
	title = models.CharField(verbose_name=_('Title'), max_length=256)
	hide_title = models.BooleanField(verbose_name=_('Hide Title'), default=False)
	slug = models.SlugField(verbose_name=_('Slug'), max_length=128)
	sub_title = models.CharField(verbose_name=_('Sub Title'), max_length=256, blank=True, null=True)
	text = models.TextField(verbose_name=_('Text'), blank=True, null=True)
	image = models.FileField(verbose_name=_('Image'), upload_to=upload_to, blank=True, null=True)
	bg = models.FileField(verbose_name=_('Background'), upload_to=upload_to, blank=True, null=True)

	# template = models.CharField(_('Template'), max_length=124, blank=True, null=True)

	pages = models.ManyToManyField(Page, related_name='blocks', verbose_name=_('Pages'), blank=True)
	order = models.PositiveSmallIntegerField(verbose_name=_('Sort ordering'), default=500)


	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)


	# def dependent_from(self):
	# 	return self.content_object

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
	image = models.FileField(verbose_name=_('Image'), upload_to=upload_to, blank=True, null=True)

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
