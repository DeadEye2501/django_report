from django.urls import path, include
from oil_report.routers import *


urlpatterns = [
    path('api/', include(report_router.urls)),
]
