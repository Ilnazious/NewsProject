from django.urls import path
from .views import PostsList, PostDetail, NewsCreateView, NewsUpdateView, NewsDeleteView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path('', PostsList.as_view(), name='news_list'),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostsList.as_view()),
# Новости
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
# Статьи
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]