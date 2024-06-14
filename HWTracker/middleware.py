from django.shortcuts import render


class CustomErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Handle error
        if 400 <= response.status_code < 600:
            username = request.session.get('username')
            if username is None:
                return render(request, 'main/error_no_nav.html', {'error_code': response.status_code}, status=response.status_code)
            return render(request, 'main/error.html', {'error_code': response.status_code}, status=response.status_code)

        return response
