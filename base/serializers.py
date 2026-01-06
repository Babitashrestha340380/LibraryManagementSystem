from rest_framework import serializers
from .models import Book, Author, Genre, BorrowRecord
from django.contrib.auth.models import User

# -----------------------------
# Author Serializer
# -----------------------------
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

# -----------------------------
# Genre Serializer
# -----------------------------
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

# -----------------------------
# Book Serializer
# -----------------------------
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        # Handle nested author
        author_data = validated_data.pop('author')
        author, _ = Author.objects.get_or_create(**author_data)

        # Handle nested genre
        genre_data = validated_data.pop('genre')
        genre, _ = Genre.objects.get_or_create(**genre_data)

        # Create book
        book = Book.objects.create(author=author, genre=genre, **validated_data)
        return book

    def update(self, instance, validated_data):
        # Update nested author
        author_data = validated_data.pop('author', None)
        if author_data:
            author, _ = Author.objects.get_or_create(**author_data)
            instance.author = author

        # Update nested genre
        genre_data = validated_data.pop('genre', None)
        if genre_data:
            genre, _ = Genre.objects.get_or_create(**genre_data)
            instance.genre = genre

        # Update remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# -----------------------------
# Borrow Record Serializer
# -----------------------------
class BorrowRecordSerializer(serializers.ModelSerializer):
    # Display book details
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), write_only=True, source='book'
    )

    member = serializers.StringRelatedField(read_only=True)  # Automatically set from request.user

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'book_id', 'member', 'issue_date', 'due_date', 'return_date']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        # Assign member
        validated_data['member'] = user.member


        # Decrease available copies
        book = validated_data['book']
        if book.available_copies <= 0:
            raise serializers.ValidationError("No copies available for this book.")
        book.available_copies -= 1
        book.save()

        borrow_record = BorrowRecord.objects.create(**validated_data)
        return borrow_record

    def update(self, instance, validated_data):
        # If returning book, increase available copies
        return_date = validated_data.get('return_date', None)
        if return_date and not instance.return_date:

            instance.book.available_copies += 1
            instance.book.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
