from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser


class JWTMiddleware:
    def resolve(self, next, root, info, **kwargs):
        request = info.context
        user = AnonymousUser()
        auth = JWTAuthentication()

        header = request.headers.get('Authorization')
        if header and header.startswith("Bearer "):
            try:
                validated_token = auth.get_validated_token(
                    header.split(" ")[1])
                user = auth.get_user(validated_token)
            except Exception:
                pass  

        request.user = user
        return next(root, info, **kwargs)
