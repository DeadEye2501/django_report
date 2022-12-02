from datetime import datetime
from .serializers import CreateDataFrameSerializer
from .kernel import main
from .models import Report


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

    for i in range(len(data['date'])):
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
