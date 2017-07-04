from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, TagForm, SearchForm
from django.core.urlresolvers import reverse
from haystack.query import SearchQuerySet
from haystack.utils import Highlighter
from django.http import JsonResponse
from django.utils import timezone
from .models import Post, Tag


def create_pagination(query, post_per_page, page):
    paginator = Paginator(query, post_per_page)  # Show 2 post per page
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return [posts, paginator.page_range, paginator.count]


def post_list(request):
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    page = request.GET.get('page')
    pagination = create_pagination(posts_list, 2, page)
    form_search = SearchForm()
    params = {'posts': pagination[0], 'n': pagination[1], 'paginator_count': pagination[2], 'form_search': form_search}
    return render(request, 'blog/post_list.html', params)


def post_with_tag(request, slug):
    tags = get_object_or_404(Tag, slug=slug)
    posts_list = tags.get_post_from_tag()
    page = request.GET.get('page')
    pagination = create_pagination(posts_list, 2, page)
    params = {'posts': pagination[0], 'n': pagination[1], 'paginator_count': pagination[2]}
    return render(request, 'blog/post_list.html', params)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required()
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form_post': form, 'new_post': True})


@login_required()
def new_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('new_tag')
    else:
        form = TagForm()
    tags_list = Tag.objects.all().order_by('slug')
    return render(request, 'blog/new_tag.html', {
        'form_tags': form, 'tags_list': tags_list})


@login_required()
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('post_detail', slug=slug)


@login_required()
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form_post': form})


@login_required()
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post_list')


def post_search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['comment']
            post_results = SearchQuerySet().models(Post).filter(content=search_text).highlight()
            params = {'form_search': form, 'post_results': post_results, 'query': search_text}
            return render(request, 'blog/post_search.html', params)
    else:
        form = SearchForm()
    return render(request, 'blog/post_search.html', {'form_search': form})


def search_modal(request):
    if request.method == "POST" and request.is_ajax():
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['comment']
            post_results = SearchQuerySet().models(Post).filter(content=search_text).highlight()
            html = '<div class="blog-post">'
            for qs in post_results:
                url_post = reverse('post_detail', kwargs={'slug': qs.object.slug})
                html += '<h2 class="blog-post-title text-center"><a class="color-black" href="%s">%s</a></h2>' % (url_post, qs.object.title)
                qs_highlight = Highlighter(search_text, html_tag='div', css_class='highlight_text')
                html += '<p class="text-justify">%s</p>' % (qs_highlight.highlight(qs.object.body))
            html += '</div>'
            data = {
                'html_results': html,
            }
            return JsonResponse(data)
