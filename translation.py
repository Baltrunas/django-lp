from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions


from .models import Block
from .models import SubBlock


class BlockTranslationOptions(TranslationOptions):
	fields = ['title', 'sub_title', 'text']

translator.register(Block, BlockTranslationOptions)


class SubBlockTranslationOptions(TranslationOptions):
	fields = ['title', 'sub_title', 'description']

translator.register(SubBlock, SubBlockTranslationOptions)
