from django.contrib import admin
from .models import Author, Genre, Book, Member, BorrowRecord

# -----------------------------
# Author Admin
# -----------------------------
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# -----------------------------
# Genre Admin
# -----------------------------
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# -----------------------------
# Book Admin
# -----------------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'isbn', 'total_copies', 'available_copies')
    list_filter = ('genre', 'author')
    search_fields = ('title', 'author__name', 'isbn')


# -----------------------------
# Member Admin
# -----------------------------
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'membership_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


# -----------------------------
# BorrowRecord Admin
# -----------------------------
@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'member', 'issue_date', 'due_date', 'return_date', 'is_overdue')
    list_filter = ('issue_date', 'due_date', 'return_date')
    search_fields = ('book__title', 'member__user__username')
    readonly_fields = ('is_overdue',)
