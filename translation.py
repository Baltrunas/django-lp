# -*- coding: utf-8 -*-
# Model Translation
from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

# Models
from .models import CountDown
from .models import FormConfig
from .models import Block
from .models import SubBlock
# from .models import FAQ
from .models import Office


class FormConfigTranslationOptions(TranslationOptions):
	fields = ['title', 'submit_name', 'phone_placeholder', 'email_placeholder', 'comment_placeholder', 'error_message', 'tnx_message']

translator.register(FormConfig, FormConfigTranslationOptions)


class CountDownTranslationOptions(TranslationOptions):
	fields = ['name']

translator.register(CountDown, CountDownTranslationOptions)


class BlockTranslationOptions(TranslationOptions):
	fields = ['title', 'sub_title', 'text']

translator.register(Block, BlockTranslationOptions)


class SubBlockTranslationOptions(TranslationOptions):
	fields = ['title', 'sub_title', 'description']

translator.register(SubBlock, SubBlockTranslationOptions)


# class FAQTranslationOptions(TranslationOptions):
# 	fields = ['problem_title', 'problem_description', 'solutions_title', 'solutions_description']

# translator.register(FAQ, FAQTranslationOptions)


# TariffAddition
# name
# description
# price


# Tariff
# title
# sub_title
# old_price
# new_price
# description
# options


class OfficeTranslationOptions(TranslationOptions):
	fields = ['name', 'description', 'orgdata', 'address', 'www']

translator.register(Office, OfficeTranslationOptions)


# Organization
# name
# description
# www


# Review
# name
# text
# result


# Document
# name
# description

# Category
# name



# Project
# name
# description
# target
# result
# result_url


