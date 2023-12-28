from django.test import TestCase
from django.utils.text import slugify

from blogs.models import Blog
from blogs.utils import slugify_instance_title

# Create your tests here.

class BlogTestCase(TestCase):
    def setUp(self):
        self.number_of_blogs = 10
        for i in range(0, self.number_of_blogs):
            Blog.objects.create(title='Hello Title', content='Hello Content')

    def test_queryset_exists(self):
        queryset = Blog.objects.all()
        self.assertTrue(queryset.exists())

    def test_queryset_count(self):
        queryset = Blog.objects.all()
        self.assertEqual(queryset.count(), self.number_of_blogs)

    def test_slug(self):
        object = Blog.objects.all().order_by("id").first()
        title = object.title
        slug = object.slug
        slugfield_title = slugify(title)
        self.assertEqual(slug, slugfield_title)

    def test_unique_slug(self):
        queryset = Blog.objects.all().exclude(slug__iexact='hello-title')
        for object in queryset:
            title = object.title
            slug = object.slug
            slugfield_title = slugify(title)
            self.assertNotEqual(slug, slugfield_title)
    
    def test_slugify_instance_title(self):
        object = Blog.objects.all().last()
        new_slugs=[]
        for i in range(0,25):
            instance = slugify_instance_title(object, save=False)
            new_slugs.append(instance.slug)
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_slugify_instance_title_redux(self):
        slug_list = Blog.objects.all().values_list('slug', flat=True)
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(slug_list), len(unique_slug_list))

    def test_article_search_manager(self):
        qs = Blog.objects.search(query='hello title')
        self.assertEqual(qs.count(), self.number_of_blogs)

        qs = Blog.objects.search(query='hello')
        self.assertEqual(qs.count(), self.number_of_blogs)

        qs = Blog.objects.search(query='hello title')
        self.assertEqual(qs.count(), self.number_of_blogs)