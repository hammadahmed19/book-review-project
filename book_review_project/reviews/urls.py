from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r"book", ReviewViewSet, basename="reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("book/<int:book_id>/", ReviewViewSet.as_view({"get": "reviews_for_book"}), name="reviews-for-book"),
]
