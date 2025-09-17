from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.db.models import Count
from book_review_project.utils.responses import custom_response
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from drf_spectacular.utils import extend_schema


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,     
        responses={201: UserSerializer},  
        description="Register a new user account",
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return custom_response("User registered successfully", UserSerializer(user).data, status.HTTP_201_CREATED)
        return custom_response("Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)


class ActiveUsersView(APIView):
    """
    Users who reviewed more than 5 books
    """
    def get(self, request):
        users = User.objects.annotate(review_count=Count("reviews")).filter(review_count__gt=5)
        data = [{"name": u.name, "review_count": u.review_count} for u in users]
        return custom_response("Active users", data)


class MostActiveUserView(APIView):
    """
    User with the maximum number of reviews
    """
    def get(self, request):
        user = User.objects.annotate(review_count=Count("reviews")).order_by("-review_count").first()
        if not user:
            return custom_response("No users found", [], status.HTTP_404_NOT_FOUND)
        data = {"name": user.name, "review_count": user.review_count}
        return custom_response("Most active user", data)
