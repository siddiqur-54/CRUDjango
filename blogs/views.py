from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from blogs.forms import BlogForm
from blogs.models import Blog
from django.http import Http404, HttpResponse
# Create your views here.


@login_required
def blog_create_view(request):
    form = BlogForm(request.POST or None)
    context = {
        "form" : form,
    }
    if form.is_valid():
        blog_object = form.save(commit=False)
        blog_object.user = request.user
        blog_object.save()

        context['form'] = BlogForm()
        context['object'] = blog_object
        context['created'] = True
        return redirect(blog_object.get_absolute_url())
    return render(request, "blogs/blog_create.html", context)


@login_required
def blog_list_search_view(request):
    query_dict = request.GET
    try:
        query = query_dict.get("query")
    except:
        query = None
    blog_object = None
    blog_search_object = None
    if query is not None:
        blog_search_object = Blog.objects.search(query=query)
    blog_object = Blog.objects.all()
    context = {
        "query" : query,
        "object_list" : blog_object,
        "object_search_list" : blog_search_object
    }
    return render(request, "blogs/blog_list_search.html", context)


@login_required
def blog_list_search_own_view(request):
    query_dict = request.GET
    try:
        query = query_dict.get("query")
    except:
        query = None
    blog_object = None
    blog_search_object = None
    if query is not None:
        blog_search_object = Blog.objects.search(query=query, user=request.user)
    blog_object = Blog.objects.search(user=request.user)
    context = {
        "query" : query,
        "object_list" : blog_object,
        "object_search_list" : blog_search_object
    }
    return render(request, "blogs/blog_list_search_own.html", context)



@login_required
def blog_detail_view(request, slug=None):
    print(slug)
    blog_object = None
    if slug is not None:
        try:
            blog_object = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            raise Http404
        except Blog.MultipleObjectsReturned:
            blog_object = Blog.objects.filter(slug=slug).first()
        except:
            raise Http404
    context = {
        "object": blog_object,
    }
    return render(request, "blogs/blog_detail.html", context=context)


@login_required
def blog_update_view(request, slug=None):
    blog_object = get_object_or_404(Blog, slug=slug, user=request.user)
    form = BlogForm(request.POST or None, instance=blog_object)
    context = {
        "form" : form,
        "object" : blog_object
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Blog Updated'
        context['updated'] = True
        return redirect(blog_object.get_absolute_url())
    return render(request, "blogs/blog_update.html", context)


@login_required
def blog_delete_view(request, slug=None):
    try:
        blog_object = Blog.objects.get(slug=slug, user=request.user)
    except Blog.DoesNotExist:
        blog_object = None
    if blog_object is None:
        raise Http404
    if request.method == "POST":
        blog_object.delete()
        return redirect("blogs:blog_list")
    context = {
        "object" : blog_object
    }
    return render(request, "blogs/blog_delete.html", context)