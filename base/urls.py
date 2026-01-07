'''from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views
from rest_framework.routers import DefaultRouter
from .views import BorrowRecordViewSet,MemberBorrowHistoryView

schema_view = get_schema_view(
    openapi.Info(
        title="Library Management API",
        default_version='v1',
        description="API documentation for LMS",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],  # Leave empty; handled per endpoint
)
router = DefaultRouter()
router.register(r'borrow-records', BorrowRecordViewSet, basename='borrow-record')


urlpatterns = [
    path('books/', views.BookListCreateView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('borrow-records/', views.BorrowRecordListView.as_view(), name='borrow-records'),
    path('my-borrow-history/', views.MemberBorrowHistoryView.as_view()),
    path("member/login/", views.MemberLoginAPIView.as_view(), name="member-login"),
         path("member/register/", views.MemberRegistrationAPIView.as_view(), name="member-register"),


          # Admin CRUD via router
    path('', include(router.urls)),

    # Member-only borrow history
    path('my-borrow-history/', MemberBorrowHistoryView.as_view(), name='my-borrow-history'),




     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
'''
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views
from rest_framework.routers import DefaultRouter
from .views import BorrowRecordViewSet, MemberBorrowHistoryView

# Swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="Library Management API",
        default_version='v1',
        description="API documentation for LMS",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

# Router for BorrowRecordViewSet (Admin CRUD)
router = DefaultRouter()
router.register(r'borrow-records', BorrowRecordViewSet, basename='borrow-record')

urlpatterns = [
    # Books
    path('books/', views.BookListCreateView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # Member-only borrow history
    path('my-borrow-history/', MemberBorrowHistoryView.as_view(), name='my-borrow-history'),

    # Member auth
    path("member/login/", views.MemberLoginAPIView.as_view(), name="member-login"),
    path("member/register/", views.MemberRegistrationAPIView.as_view(), name="member-register"),

    # Admin CRUD via router
    path('', include(router.urls)),



    # Swagger / Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]



