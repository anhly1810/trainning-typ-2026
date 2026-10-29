from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio", "created_at"]


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "author_name",
            "price",
            "published_year",
            "quantity",
            "created_at",
            "updated_at",
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("price must be >= 0")
        return value

    def validate_published_year(self, value):
        if value < 1440 or value > 2100:
            raise serializers.ValidationError("published_year is out of range")
        return value
