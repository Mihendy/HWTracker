import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from main.views import logger
from .models import Post
from main.functions import authorized_only, editor_only


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
