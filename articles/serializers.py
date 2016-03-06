from rest_framework import serializers
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.first_name')
    snippet = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'title', 'slug', 'snippet', 'author'
        )

    def get_snippet(self, article):
        return article.body[:200]+"..."


class ArticleDetailSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.first_name')
    category_slug = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'title', 'slug', 'author',
            'published_at', 'category_slug', 'hero_image',
            'content_image', 'updated_at', 'body'
        )

    def get_category_slug(self, article):
        return article.category.slug


class ArticlePreviewSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.first_name')
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
