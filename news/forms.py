from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'author', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is not None and len(title) > 150:
            raise ValidationError({
                "title": "Заголовок не может содержать более 150 символов"
            })

        text = cleaned_data.get("text")
        if text == title:
            raise ValidationError(
                "Текст не должен быть идентичен заголовку."
            )
        return cleaned_data


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
