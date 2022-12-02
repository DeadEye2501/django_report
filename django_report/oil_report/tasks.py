from django_report.celery import app
from .kernel import main
from datetime import datetime, date
from .models import Report
from .serializers import CreateDataFrameSerializer


@app.task
def create_data_frame(report_id, data):
    start = datetime.now()
    report = Report.objects.get(pk=report_id)
    report.status = Report.STATUS_CHOICES[1]
    report.save()

    resp = dict(main(**data))
    data = {'water': [], 'oil': [], 'wct': [], 'liquid': [], 'date': []}

    for key, value in resp.items():
        for item in value:
            data[key].append(item)

    for i in range(count := len(data['date'])):
        print(i, count)
        current_data = {
            'water': data['water'][i],
            'oil': data['oil'][i],
            'wct': data['wct'][i],
            'liquid': data['liquid'][i],
            'date': data['date'][i].date(),
            'report': report_id,
        }
        serializer = CreateDataFrameSerializer(data=current_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    finish = datetime.now() - start
    report.calc_time = finish.seconds + (finish.microseconds / 1000000)
    report.status = Report.STATUS_CHOICES[0]
    report.save()
