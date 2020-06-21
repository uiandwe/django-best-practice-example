from django_filters import FilterSet, CharFilter, NumberFilter, BooleanFilter
from django_filters.filters import OrderingFilter

from .models import Post


class PostFilter(FilterSet):
    count = NumberFilter()
    count__gt = NumberFilter(field_name="count", lookup_expr="gt")
    count__lt = NumberFilter(field_name="count", lookup_expr="lt")
    public = BooleanFilter(field_name="public")
    message = CharFilter(lookup_expr="icontains")
    owner__name = CharFilter(field_name="owner", lookup_expr="username__icontains")

    order_by_field = "ordering"
    ordering = OrderingFilter(fields=("message", "count", "public"))

    class Meta:
        model = Post
        fields = ["message", "count", "public"]

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
