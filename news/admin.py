from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

admin.site.register(Post)
admin.site.register(Category)


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post
