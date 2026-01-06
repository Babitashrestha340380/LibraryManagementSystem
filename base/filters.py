import django_filters
from .models import Book,BorrowRecord

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    genre_name = django_filters.CharFilter(field_name='genre__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author_name', 'genre_name']


class BorrowRecordFilter(django_filters.FilterSet):
    member_name = django_filters.CharFilter(field_name='member__username', lookup_expr='icontains')
    issue_date = django_filters.DateFromToRangeFilter()
    due_date = django_filters.DateFromToRangeFilter()
    return_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = BorrowRecord
        fields = ['member_name', 'issue_date', 'due_date', 'return_date']