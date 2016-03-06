from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Article
from .serializers import (
    ArticleListSerializer, ArticleDetailSerializer,
    ArticlePreviewSerializer, NextArticleToReadSerializer
)


class ArticleViewSet(viewsets.ViewSet):
    """
    A view with all the actions related to the article.
    """
    permission_classes = (AllowAny,)

    def list(self, request):
        """
        Show the list of articles available
        """

        articles = Article.objects.filter(is_published=True)[:10]
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    def detail(self, request, slug=None):
        """
        Show a blog post
        """

        queryset = Article.objects.all()
        article = get_object_or_404(queryset, slug=slug)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)


class RecommendedArticleViewSet(viewsets.ViewSet):
    """
    A view with all the actions related to the recommended articles.
    """
    permission_classes = (AllowAny,)

    def random_article_preview(self, request):
        """
        Fetch a random article for preview
        """

        article = Article.objects.all().order_by('?')[:1][0]
        serializer = ArticlePreviewSerializer(article)
        return Response(serializer.data)

    def what_to_read_next(self, request):
        """
        Get related articles for the user to read,
        If nothing show him the latest.
        """
        current_article = request.GET.get('current_article', None)
        category = request.GET.get('category', None)

        article_set = None
        if category and current_article:
            article_set = Article.objects.exclude(id=current_article).filter(category__id=category)

        if article_set.count() < 5:
            article_set = article_set | Article.objects.exclude(
                slug=current_article
            ).exclude(id__in=article_set)[:article_set.count()]

        serializer = NextArticleToReadSerializer(article_set[:4], many=True)
        return Response(serializer.data)
