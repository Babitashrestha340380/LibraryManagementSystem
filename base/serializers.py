from rest_framework import serializers
from .models import Book, Author, Genre, BorrowRecord
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction

from base.models import Member
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from base.permissions import IsAdmin  # Admin-only permission

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
'''class BorrowRecordSerializer(serializers.ModelSerializer):
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
        return instance'''


'''class BorrowRecordSerializer(serializers.ModelSerializer):
    # Display book details
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), write_only=True, source='book'
    )
    member = serializers.StringRelatedField(read_only=True)  # Auto from request.user

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
        return instance'''


class BorrowRecordSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True,
        source='book'
    )
    member = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = [
            'id',
            'book',
            'book_id',
            'member',
            'issue_date',
            'due_date',
            'return_date'
        ]



class MemberLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        allow_blank=False,
        trim_whitespace=True
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False
    )




class MemberRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    @transaction.atomic
    def create(self, validated_data):
        # Remove confirm_password, we don't need to store it
        validated_data.pop("confirm_password")

        # Create the user
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"]
        )

        # Create member profile safely
        Member.objects.get_or_create(user=user)

        # RETURN THE USER INSTANCE!!! ✅ DRF expects an object
        return user