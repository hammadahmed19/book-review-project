from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly ,IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Review
from .serializers import ReviewSerializer
from books.models import Book
from book_review_project.utils.responses import custom_response


class ReviewPagination(PageNumberPagination):
    page_size = 10


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "book").all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ReviewPagination

    def perform_create(self, serializer):
        # Assign request.user as review author; UniqueConstraint prevents duplicates
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Prevent duplicate review per user-book combo
        book_id = request.data.get("book")
        if Review.objects.filter(user=request.user, book_id=book_id).exists():
            return custom_response("You have already reviewed this book", None, status_code=400)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Custom response wrapper
        qs = self.filter_queryset(self.get_queryset()).order_by("-created_at")
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def reviews_for_book(self, request, book_id=None):
        # Get all reviews for a given book
        book = get_object_or_404(Book, pk=book_id)
        qs = Review.objects.filter(book=book).select_related("user").order_by("-rating", "-created_at")
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
