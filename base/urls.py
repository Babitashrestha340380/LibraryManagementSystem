from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Library Management System API",
      default_version='v1',
      description="API documentation for LMS",
      contact=openapi.Contact(email="your_email@example.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('books/', views.BookListCreateView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('borrow-records/', views.BorrowRecordListView.as_view(), name='borrow-records'),
    path('my-borrows/', views.MemberBorrowHistoryView.as_view(), name='my-borrows'),

     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
