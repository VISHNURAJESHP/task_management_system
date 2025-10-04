import jwt
from django.conf import settings
from .models import User
from rest_framework.exceptions import AuthenticationFailed

def get_token_from_request(request):
    # Get token from cookies
    token = request.COOKIES.get("jwt")
    
    if not token:
        return None

    try:
        # Decode JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")
        return User.objects.filter(id=user_id).first()
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return None
