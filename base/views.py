# library/views.py
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Book, BorrowRecord
from .serializers import BookSerializer, BorrowRecordSerializer
from .permissions import IsAdmin, IsMember
from .pagination import LMSResultsSetPagination
from .filters import BookFilter, BorrowRecordFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from .models import Member
from rest_framework.response import Response
from django.contrib.auth import authenticate,login 
from rest_framework.authtoken.models import Token





# -----------------------------
# Books
# -----------------------------
class BookListCreateView(generics.ListCreateAPIView):
    """
    GET /books/:
        - List all books (Members & Admins)
        - Filters: title, author_name, genre_name
        - Pagination supported
    POST /books/:
        - Create a new book (Admin only)
        - Required JSON: title, isbn, total_copies, available_copies, author{name}, genre{name}
    Permissions:
        - GET: Authenticated
        - POST: Admin only
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    pagination_class = LMSResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name', 'genre__name']

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [p() for p in permission_classes]
    
    
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /books/<id>/ : Retrieve book details (Members & Admins)
    PUT /books/<id>/ : Update book (Admins only)
    PATCH /books/<id>/ : Partial update (Admins only)
    DELETE /books/<id>/ : Delete book (Admins only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:  # GET
            permission_classes = [IsAuthenticated]
        return [p() for p in permission_classes]

# -----------------------------
# Borrow Records
# -----------------------------
class BorrowRecordListView(generics.ListAPIView):
    """
    GET /borrow-records/:
        - List all borrow records (Admin only)
        - Filters: member_name, issue_date, due_date, return_date
        - Pagination supported
    Permissions:
        - Admin only
    """
    queryset = BorrowRecord.objects.all().order_by('-issue_date')
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = LMSResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BorrowRecordFilter
    search_fields = ['member__username', 'book__title']

class MemberBorrowHistoryView(generics.ListAPIView):
    """
    GET /my-borrow-history/:
        - List borrowing history for the logged-in member
        - Pagination supported
    Permissions:
        - Member only
    """
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LMSResultsSetPagination

    def get_queryset(self):
        # Only non-staff users can access
        if self.request.user.is_staff:
            raise PermissionDenied("Librarians cannot access this endpoint.")

        # Safely get the Member instance
        try:
            member = self.request.user.member
        except Member.DoesNotExist:
            raise PermissionDenied("This user has no member profile.")

        return BorrowRecord.objects.filter(member=member).order_by('-issue_date')
    
    