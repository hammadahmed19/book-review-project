from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg, Count

from .models import Book
from .serializers import BookSerializer
from book_review_project.utils.responses import custom_response


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # annotate avg rating + review count on all queries
        return Book.objects.annotate(
            avg_rating=Avg("reviews__rating"),
            review_count=Count("reviews")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return custom_response("Books retrieved successfully", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(book)
        return custom_response("Book retrieved successfully", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custom_response("Book created successfully", serializer.data, status_code=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custom_response("Book updated successfully", serializer.data)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()
        return custom_response("Book deleted successfully", None, status_code=204)

    

    def top_rated_books(self, request):
        print("called")
        books = (
            Book.objects.annotate(
                avg_rating=Avg("reviews__rating"),
                review_count=Count("reviews"),
            )
            .filter(review_count__gt=0)  # exclude books with no reviews
            .order_by("-avg_rating", "-review_count")[:3]
        )

        data = [
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "avg_rating": round(b.avg_rating or 0, 2),
                "review_count": b.review_count,
            }
            for b in books
        ]
        return custom_response("Top 3 highest-rated books", data)

    

