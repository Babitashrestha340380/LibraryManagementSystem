from django.db import models
from django.contrib.auth.models import User
from datetime import date

# -----------------------------
# Member Profile Model
# -----------------------------
class Member(models.Model):
    """
    Extends Django User model.
    Each user is either Admin or Member.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# -----------------------------
# Author Model
# -----------------------------
class Author(models.Model):
    """
    Stores author details
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -----------------------------
# Genre Model
# -----------------------------
class Genre(models.Model):
    """
    Stores book genres
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# -----------------------------
# Book Model
# -----------------------------
class Book(models.Model):
    """
    Stores book information
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    isbn = models.CharField(max_length=20, unique=True)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()

    def __str__(self):
        return self.title


# -----------------------------
# Borrow Record Model
# -----------------------------
'''class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def is_overdue(self):
        """
        Checks if book is overdue
        """
        if self.due_date is None:
            return False
        return self.return_date is None and date.today() > self.due_date

    is_overdue.boolean = True
    is_overdue.short_description = "Overdue?"

    def __str__(self):
        return f"{self.book.title} - {self.member.user.username}"'''

# -----------------------------
# Borrow Record Model
# -----------------------------
class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ("BORROWED", "Borrowed"),
        ("RETURNED", "Returned"),
        ("OVERDUE", "Overdue"),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="BORROWED",
        help_text="Current status of the borrow record"
    )

    def is_overdue(self):
        """
        Checks if book is overdue
        """
        if self.due_date is None:
            return False
        return self.return_date is None and date.today() > self.due_date

    is_overdue.boolean = True
    is_overdue.short_description = "Overdue?"

    def __str__(self):
        return f"{self.book.title} - {self.member.user.username} ({self.status})"
