from django.contrib import admin

from .models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'is_published',
        'published_at',
        'category',
        'created_at',
        'updated_at',
    )
    prepopulated_fields = {'slug': ('title',)}

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.prepopulated_fields = {}
            return self.readonly_fields + ('slug',)
        return self.readonly_fields
admin.site.register(Article, ArticleAdmin)

admin.site.register(Category)
