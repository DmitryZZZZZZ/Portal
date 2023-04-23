from django.contrib.auth.models import User
from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post


class PostFilter(FilterSet):
    author__user = ModelChoiceFilter(
        field_name='author__author',
        queryset=User.objects.all(),
        label='Автор',
        empty_label='All'
    )
    time_in = DateFilter(
        lookup_expr='gt',
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }