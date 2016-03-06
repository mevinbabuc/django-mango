from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({}, status=404)

    def detail(self, request, slug=None):
        """
        Show a blog post
        """

        queryset = Article.objects.all()
        article = get_object_or_404(queryset, slug=slug)
        serializer = ArticleDetailSerializer(article)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({}, status=404)


class RecommendedArticleViewSet(viewsets.ViewSet):
    """
    A view with all the actions related to the recommended articles.
    """
    permission_classes = (AllowAny,)

    def random_article_preview(self, request):
        """
        Fetch a random article for preview
        """
        article = Article.objects.all().order_by('?').first()
        try:
            serializer = ArticlePreviewSerializer(article)
        except:
            return Response({}, status=404)
        else:
            return Response(serializer.data)

    def what_to_read_next(self, request):
        """
        Get related articles for the user to read,
        If nothing show him the latest.
        """
        current_article = request.GET.get('current_article', None)
        category = request.GET.get('category', None)
        page = request.GET.get('page', None)
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
            article_set = Article.objects.exclude(slug=current_article)

        pages = Paginator(article_set, 4)
        try:
            article_set = pages.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            print "not an interger"
            article_set = pages.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            article_set = pages.page(pages.num_pages)

        serializer = NextArticleToReadSerializer(article_set, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({}, status=404)
