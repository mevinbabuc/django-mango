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
        NO_OF_ARTICLES = 4

        if current_article:
            article_set = Article.objects.exclude(slug=current_article)

        if category:
            article_set = article_set.filter(category__slug=category)

        if article_set:
            if article_set.count() < NO_OF_ARTICLES:
                article_set = article_set | Article.objects.exclude(slug=current_article)[:NO_OF_ARTICLES - article_set.count()]
        else:
            article_set = Article.objects.all()

        serializer = NextArticleToReadSerializer(article_set.order_by('?')[:NO_OF_ARTICLES], many=True)
        return Response(serializer.data)
