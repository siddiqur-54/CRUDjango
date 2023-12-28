from django.urls import path
from blogs.views import (
    blog_create_view,
    blog_list_search_view,
    blog_detail_view,
    blog_delete_view,
    blog_update_view,
    blog_list_search_own_view,
)

app_name = 'blogs'

urlpatterns = [
    path('blog-list-own/', blog_list_search_own_view, name='blog_list_search_own'),
    path('create/', blog_create_view, name='blog_create'),
    path('<slug:slug>/', blog_detail_view, name='blog_detail'),
    path('<slug:slug>/update/', blog_update_view, name='blog_update'),
    path('<slug:slug>/delete/', blog_delete_view, name='blog_delete'),
    path('', blog_list_search_view, name='blog_list_search'),
]