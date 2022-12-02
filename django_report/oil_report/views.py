from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import *
from oil_report.tasks import *


class ReportPagination(PageNumberPagination):
    page_size = 10


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = GetReportsSerializer
    pagination_class = ReportPagination

    def retrieve(self, request, *args, **kwargs):
        fields = self._parse_query_params(request.query_params)
        instance = self.get_object()
        serializer = GetReportSerializer(instance, fields=fields)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CreateReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.save()
        create_data_frame.delay(report.id, request.data)
        headers = self.get_success_headers(serializer.data)
        return Response({'report_id': report.id}, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def _parse_query_params(query_params):
        fields = query_params.get('fields')
        if fields:
            return fields.replace("'", '').replace('{', '').replace('}', '').replace(' ', '').split(',')
        else:
            return []
