from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['themes']


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ['title', 'text']
