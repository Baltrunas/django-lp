from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

from .models import FormConfig
from .models import Block
from .models import SubBlock
from .models import FAQ


class BlockTranslationOptions(TranslationOptions):
	fields = ['title', 'sub_title', 'text']

translator.register(Block, BlockTranslationOptions)


class SubBlockTranslationOptions(TranslationOptions):
	fields = ['title', 'sub_title', 'description']

translator.register(SubBlock, SubBlockTranslationOptions)


class FAQTranslationOptions(TranslationOptions):
	fields = ['problem_title', 'problem_description', 'solutions_title', 'solutions_description']

translator.register(FAQ, FAQTranslationOptions)
