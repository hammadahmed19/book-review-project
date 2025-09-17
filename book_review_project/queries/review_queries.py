from books.models import Book
from reviews.models import Review
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count

User = get_user_model()

def top_books():
    qs = (
        Book.objects.annotate(
            avg_rating=Avg("reviews__rating"),
            review_count=Count("reviews"),
        )
        .filter(review_count__gt=0)   # only include books with reviews
        .order_by("-avg_rating", "-review_count")[:3]
        .values("title", "avg_rating", "review_count")
    )
    return list(qs)


def active_users():
    qs = (
        User.objects.annotate(
            review_count=Count("reviews")  
        )
        .filter(review_count__gt=5)
        .values("name", "review_count")
    )
    return list(qs)

def most_active_user():
    qs = (
        User.objects.annotate(review_count=Count("reviews"))
        .order_by("-review_count")
        .values("name", "review_count")
        .first()
    )
    return qs


def reviews_for_book(book_id):
    qs = (
        Review.objects.filter(book_id=book_id)
        .select_related("user")
        .order_by("-rating")
        .values("user__name", "rating", "review_text")
    )
    return list(qs)
