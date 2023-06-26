from django.contrib import admin
from django.urls import path, include
from news.views import IndexView
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', IndexView.as_view()),
]

urlpatterns += doc_urls
