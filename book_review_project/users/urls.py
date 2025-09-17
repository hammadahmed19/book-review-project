from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet,
    UserRegisterView,
    ActiveUsersView,
    MostActiveUserView
)

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("active-users/", ActiveUsersView.as_view(), name="active-users"),
    path("most-active/", MostActiveUserView.as_view(), name="most-active-user"),
    path("", include(router.urls)),
]
