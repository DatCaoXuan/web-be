from django_filters import FilterSet, CharFilter, NumberFilter
from django.db.models import Q, Count
from .models import Book
from functools import reduce
from operator import or_

class BookFilter(FilterSet):

	genres = CharFilter(field_name='genres__id', method='filter_genres')
	book_type = CharFilter(field_name='book_type')
	search = CharFilter(method='filter_search')
	author = CharFilter(field_name='authors__name', method='filter_author')
	start = NumberFilter(method='filter_empty')
	limit = NumberFilter(method='filter_empty')

	class Meta:
		model = Book
		fields = []

	def filter_queryset(self, queryset):
		queryset = super().filter_queryset(queryset)
		start_filter = self.form.cleaned_data['start'] or 0
		limit_filter = self.form.cleaned_data['limit'] or 10

		return queryset[start_filter:start_filter + limit_filter]

	def filter_empty(self, queryset, name, value):	
		return queryset

	def filter_author(self, queryset, name, value):
		if not value:
			return queryset

		return queryset.filter(Q(**dict([(f'{name}__icontains', value), ]))).distinct()

	def filter_search(self, queryset, name, value):
		if not value:
			return queryset
		
		return queryset.filter(Q(title__icontains=value) | Q(slug__icontains=value))

	def filter_genres(self, queryset, name, value):
		if not value:
			return queryset
		
		values = list(set(value.split(',')))
		query = reduce(
			or_, 
			(Q(**dict([(name, _), ])) for _ in values[1:]), 
			Q(**dict([(name, values[0]), ]))
		)
		id_set = queryset.filter(query).values('id').annotate(cnt=Count('id')).filter(cnt__gte=len(values))

		return queryset.filter(pk__in=[_ for _ in id_set.values_list('id', flat=True).distinct()])
