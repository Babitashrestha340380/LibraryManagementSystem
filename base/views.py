from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Book, BorrowRecord
from .serializers import BookSerializer, BorrowRecordSerializer
from .permissions import IsAdmin, IsMember
from .pagination import LMSResultsSetPagination


# -----------------------------
# Book Views
# -----------------------------

class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: List all books (Members & Admins)
    POST: Create a new book (Admins only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated, IsAdmin]
        else:  # GET
            permission_classes = [IsAuthenticated]
        return [p() for p in permission_classes]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve book details (Members & Admins)
    PUT/PATCH/DELETE: Update/Delete book (Admins only)
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
# Borrow Records Views
# -----------------------------

class BorrowRecordListView(generics.ListAPIView):
    """
    Admins can view all borrowing records.
    """
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = LMSResultsSetPagination


class MemberBorrowHistoryView(generics.ListAPIView):
    """
    Members can view their own borrowing history.
    """
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated, IsMember]
    pagination_class = LMSResultsSetPagination

    def get_queryset(self):
        return BorrowRecord.objects.filter(member=self.request.user)
    
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = LMSResultsSetPagination



class BookListView(ListAPIView):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    pagination_class = LMSResultsSetPagination