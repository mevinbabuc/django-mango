from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Article(models.Model):
    """
    Model where the content of the blog post is saved and managed
    Each post requires to have a unique title and the user has the ability to
    publish or not publish the post. The User can also categorize the posts, which helps
    in generating better recommendation for the user
    """
    title = models.CharField(max_length=255, unique=True, blank=False, help_text='Title of the Article', db_index=True)
    slug = models.SlugField()

    author = models.ForeignKey(User)
    is_published = models.BooleanField(default=False, help_text='Do you want to publish this article ?')
    published_at = models.DateTimeField(help_text='Date the article was published at')
    category = models.ForeignKey('articles.Category', help_text='Category this article belongs to')
    body = models.TextField(blank=False)

    hero_image = models.ImageField(upload_to='hero', blank=True, null=True, help_text="Hero image for the blog")
    content_image = models.ImageField(upload_to='content', blank=True, null=True, help_text="optional image to be included in the content")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-published_at", "-updated_at"]

    def __unicode__(self):
        return self.title + " by " + self.author.username

    def save(self, *args, **kwargs):
        # Check if a new post is being created
        if not self.id:
            # Do not let updates to the title change the url.
            # URLs should be permanent
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)


class Category(models.Model):
    """
    Stores unique blog post categories
    """
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title
