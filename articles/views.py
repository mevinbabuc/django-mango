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

        queryset = Article.objects.filter(is_published=True)
        article = get_object_or_404(queryset, slug=slug)
        serializer = ArticleDetailSerializer(article)

        if serializer.data:
            return Response(serializer.data)
        else:
            return Response({}, status=404)

    def search(self, request):
        """
        Returns the top 10 search results matching,
        the title of the blog
        """
        query = request.GET.get('query', None)
        article_set = Article.objects.filter(is_published=True)

        # If query is provided search for it or return everything
        if query:
            article_set = article_set.filter(title__icontains=query)[:10]

        serializer = ArticleListSerializer(article_set, many=True)

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
        article = Article.objects.filter(is_published=True).order_by('?').first()

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

        # exclude the article the user is currently reading
        if current_article:
            article_set = Article.objects.exclude(slug=current_article)

        # Prefer to get articles from the same category the user is currently reading
        if category:
            article_set = article_set.filter(category__slug=category)

        # Check if we have a minimum of 4 articles to show based on the user
        # else fill with other articles
        if article_set:
            if article_set.count() < NO_OF_ARTICLES:
                article_set = article_set | Article.objects.exclude(slug=current_article)[:NO_OF_ARTICLES - article_set.count()]
        else:
            article_set = Article.objects.exclude(slug=current_article)

        # Create a pagination to show 4 recommendations at a time
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
