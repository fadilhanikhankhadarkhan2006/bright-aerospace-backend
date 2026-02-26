from django.shortcuts import render

# Create your views here.



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from .models import User
from .validators import validate_strong_password


@api_view(['POST'])
def register_user(request):
    """
    API to register a new user (student/company/admin)
    """

    data = request.data

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "student")

    
    if not username or not email or not password:
        return Response(
            {"error": "username, email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

  
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already registered"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_strong_password(password)
    except ValidationError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

 
    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password),
        role=role
    )

    return Response(
        {
            "message": "User registered successfully",
            "username": user.username,
            "role": user.role
        },
        status=status.HTTP_201_CREATED
    )
