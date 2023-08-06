from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.http import JsonResponse

from .functions import *


class BaseResponse:
    result = None
    result_count = 0
    limit = 20
    offset = 0

    def success_response(self, result=None, many=False, message="success", status_code=status.HTTP_200_OK):
        data = {
            'code': 1,
            "status_code": status_code,
            'msg': message,
            'data': result
        }

        if many:
            data['total'] = self.result_count

        return JsonResponse(data)

    @staticmethod
    def error_response(message="Erreur survenue lors du traitement", status_code=status.HTTP_400_BAD_REQUEST):
        data = {
            "code": 0,
            "status_code": status_code,
            "message": message,
            'data': []
        }
        return JsonResponse(data)

    class Meta:
        abstract = True


class BaseQueryAPI(APIView, BaseResponse):
    model_class = None
    serializer_class = None
    form_filter = None
    queryset = None

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model_class is not None:
            queryset = find_all(self.model_class, {})
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )

        return queryset

    def compute_query(self, id=None):
        if id is not None:
            query_set = find(self.model_class, {'id': id})
            self.result = query_set
            return {
                'qs': query_set,
                'count': 0
            }

        request_params = self.request.GET.dict()
        limit = int(request_params.get('limit', self.limit))
        offset = int(request_params.get('offset', self.offset))

        queryset = self.get_queryset()

        filters = self.form_filter(self.request.GET, queryset=queryset)
        query_set = filters.qs if int(limit) < 0 else filters.qs[offset:offset + limit]

        self.result = query_set
        self.result_count = filters.qs.count()

        return {
            'qs': query_set,
            'count': filters.qs.count()
        }


class CustomAPIView(BaseQueryAPI):

    def get(self, request):
        self.compute_query()
        serializer = self.serializer_class(self.result, many=True)
        return self.success_response(serializer.data, True)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid()
            serializer.save()
            return self.success_response(result=serializer.data, status_code=status.HTTP_201_CREATED)
        except APIException as ex:
            return self.error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomAPIDetailView(BaseQueryAPI):
    def get(self, request, id, **kwargs):
        self.compute_query(id)
        serializer = self.serializer_class(self.result)
        return self.success_response(serializer.data)

    def put(self, request, id):
        data = find(self.model_class, {'id': id})
        serializer = self.serializer_class(data, data=request.data)
        try:
            serializer.is_valid()
            serializer.save()
            return self.success_response(result=serializer.data, status_code=status.HTTP_202_ACCEPTED)
        except APIException as ex:
            return self.error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
