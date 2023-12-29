import jwt
from django.http import JsonResponse
from auth0.authentication import GetToken
from .settings import AUTH0_DOMAIN, API_AUDIENCE

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = auth_header.split(' ')[-1]

        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            if payload['iss'] != f'https://{AUTH0_DOMAIN}/' or (payload['aud'] != API_AUDIENCE and API_AUDIENCE not in payload['aud']):
                raise jwt.InvalidTokenError

            # Add user to request object
            request.user = payload
        except (jwt.InvalidTokenError, IndexError, KeyError):
            return JsonResponse({"detail": "Invalid token"}, status=401)

        response = self.get_response(request)
        return response
