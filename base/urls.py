from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListCreateView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('borrow-records/', views.BorrowRecordListView.as_view(), name='borrow-records'),
    path('my-borrows/', views.MemberBorrowHistoryView.as_view(), name='my-borrows'),
]
