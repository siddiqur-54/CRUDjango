from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from blogs.utils import slugify_instance_title

User = settings.AUTH_USER_MODEL

# Create your models here.

class BlogQuerySet(models.QuerySet):
    def search(self, query=None, user=None):
        if query is None or query == "":
            if user is not None:
                return self.filter(user=user)
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        queryset = self.filter(lookups)
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset
    

class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)
    def search(self, query=None, user=None):
        return self.get_queryset().search(query=query, user=user)


class Blog(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)

    objects = BlogManager()

    @property
    def name(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogs:blog_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

def blog_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)
pre_save.connect(blog_pre_save, sender=Blog)

def blog_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)
post_save.connect(blog_post_save, sender=Blog)