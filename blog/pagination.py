# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from collections import OrderedDict


class CustomResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"


class CustomMakePagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def paginate_queryset(self, queryset, request, view=None):
        # page_size를 가져옵니다.
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        """
        django_paginator_class는 django의 Paginator (django/core/paginator.py) 클래스로 pagination의 전체 동작을 담당합니다. 
        page_size와 queryset을 pagniator 객체를 선언합니다. 
        """
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)

        try:
            # 가져온 paginator중에서 사용자가 지정한 페이지를 가져 옵니다.
            self.page = paginator.page(page_number)
        except InvalidPage as e:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(e)
            )
            raise NotFound(msg)

        return list(self.page)

    def get_paginated_response(self, data):
        # pagination의 리턴시 보여줄 데이터 객체 입니다.
        return Response(
            OrderedDict([("count", self.page.paginator.count), ("results", data)])
        )
