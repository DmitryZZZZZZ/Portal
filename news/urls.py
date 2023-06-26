from django.urls import path, include
from rest_framework import routers
from .views import *
from django.views.decorators.cache import cache_page


router = routers.DefaultRouter()
router.register(r'news', NewsViewSet, basename='news'),
router.register(r'articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('', (PostsList.as_view()), name='post_list'),
    path('api/', include(router.urls)),
    path('<int:pk>', cache_page(60 * 10)(PostDetail.as_view()), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
