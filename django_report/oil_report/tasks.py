from django_report.celery import app
from .utils import create_data_frame as create


@app.task
def create_data_frame(report_id, data):
    create(report_id, data)
