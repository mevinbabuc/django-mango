from rest_framework import serializers
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.username')
    snippet = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'title', 'slug', 'snippet', 'author'
        )

    def get_snippet(self, article):
        return article.body[:200]+"..."


class ArticleDetailSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.username')

    class Meta:
        model = Article
        fields = (
            'title', 'slug', 'author',
            'published_at', 'category', 'hero_image',
            'content_image', 'updated_at', 'body'
        )


class ArticlePreviewSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.username')
    snippet = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'title', 'slug', 'author',
            'published_at', 'hero_image',
            'snippet'
        )

    def get_snippet(self, article):
        return article.body[:300]+"..."


class NextArticleToReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'title', 'slug', 'hero_image',
        )

    def get_snippet(self, article):
        return article.body[:300]+"..."
