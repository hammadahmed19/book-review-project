from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r"", BookViewSet, basename="books")

urlpatterns = [
    path("top-rated/", BookViewSet.as_view({"get": "top_rated_books"}), name="top-rated-books"),
    path("", include(router.urls)),
]
