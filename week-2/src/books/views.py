from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .pagination import StandardPagination


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("-id")
    serializer_class = AuthorSerializer
    pagination_class = StandardPagination


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__name"]
    ordering_fields = ["price", "published_year", "created_at", "id"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"code": status.HTTP_200_OK, "message": "Book deleted", "details": None},
            status=status.HTTP_200_OK,
        )
