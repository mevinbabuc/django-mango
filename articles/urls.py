from django.conf.urls import url
from django.views.generic import TemplateView

from .views import ArticleViewSet, RecommendedArticleViewSet


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='blog_index_page'),

    url(r'^articles/$', ArticleViewSet.as_view({'get': 'list'}), name="view_article_list"),

    url(r'^articles/preview/$', RecommendedArticleViewSet.as_view({'get': 'random_article_preview'}), name="view_random_article_preview"),
    url(r'^articles/recommend/(?P<category>[-\w]+)/(?P<current_article>[-\w]+)/$', RecommendedArticleViewSet.as_view({'get': 'what_to_read_next'}), name="view_what_to_read_next"),

    url(r'^articles/(?P<slug>[-\w]+)/$', ArticleViewSet.as_view({'get': 'detail'}), name="view_article_detail"),
]
