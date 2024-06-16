from django.shortcuts import render
from http.client import responses


class CustomErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Handle error
        if 400 <= response.status_code < 600:
            username = request.session.get('username')
            error_text = responses.get(response.status_code, 'Unknown')
            if response.status_code == 404:
                error_text = 'Мы не нашли такой страницы 👀'
            if response.status_code == 403:
                error_text = 'Ваши права доступа не позволяют перейти на эту страницу.'

            if username is None:
                return render(request, 'error_no_nav.html', {
                    'error_text': error_text,
                    'error_code': response.status_code
                }, status=response.status_code)

            user = request.user
            group = user.group
            return render(request, 'error.html', {
                'user': request.user,
                'error_code': response.status_code,
                'error_text': error_text,
                'group': group.name if group is not None else 'Нет группы'
            }, status=response.status_code)

        return response
