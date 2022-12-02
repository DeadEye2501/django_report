from rest_framework import routers
from oil_report.views import *


report_router = routers.SimpleRouter()
report_router.register(r'report', ReportViewSet)
