import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.functions import authorized_only, editor_only, errors_to_text
from main.views import logger

from .forms import PostForm
from .models import Post


@authorized_only
def post_list(request):
    template_name = 'posts/post_list.html'
    posts = Post.objects.all()
    user = request.user
    group = user.group

    return render(request, template_name,
                  {'posts': posts, 'group': group.name if group is not None else 'Нет группы'})


@authorized_only
def post_detail(request, post_slug):
    template_name = 'posts/post_detail.html'
    post = get_object_or_404(Post, slug=post_slug)
    user = request.user
    group = user.group
    return render(request, template_name, {'post': post, 'group': group.name if group is not None else 'Нет группы'})


@require_POST
@authorized_only
@editor_only
def delete_post(request):
    data = json.loads(request.body)
    post_id = data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
    except Post.DoesNotExist:
        logger.warning(f"Post with id={post_id} does not exist")
        return JsonResponse({'success': False})

    return JsonResponse({'success': True})


@authorized_only
@editor_only
def add_post_form(request, post_slug=None):
    template_name = 'posts/add_post_form.html'

    if post_slug:
        # Editing an existing task
        page_title = 'Изменение'
        post = get_object_or_404(Post, slug=post_slug)
        form = PostForm(request.POST or None, instance=post)
    else:
        # Creating a new task
        page_title = 'Создание'
        form = PostForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            if post_slug:
                post.title = form.cleaned_data["title"]
                post.slug = form.cleaned_data["slug"]
                post.body = form.cleaned_data["body"]
                post.author = request.user
                post.save()
            else:
                new_post = Post(
                    title=form.cleaned_data["title"],
                    slug=form.cleaned_data["slug"],
                    body=form.cleaned_data["body"],
                    author=request.user
                )
                new_post.save()

            return redirect("/posts")
        else:
            out = errors_to_text(form)

            return render(request, template_name,
                          {'page': page_title, 'user': request.user, "form": form, "form_errors": out})

    return render(request, template_name, {'page': page_title, 'user': request.user, "form": form})
