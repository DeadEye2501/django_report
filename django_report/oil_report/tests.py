from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date
from .models import *


class OilReportTestCase(APITestCase):
    def setUp(self):
        # report 1
        report1 = Report.objects.create(name='report 1', date_start=date(2022, 11, 10), calc_time=10.1,
                                        date_fin=date(2022, 12, 1), lag=10, status=Report.STATUS_CHOICES[0])
        DataFrame.objects.create(report=report1, date=date(2022, 11, 10), water=0.1, oil=2.4, wct=1.2, liquid=1.1)
        DataFrame.objects.create(report=report1, date=date(2022, 11, 20), water=0.2, oil=2.3, wct=2.2, liquid=4.2)
        DataFrame.objects.create(report=report1, date=date(2022, 11, 30), water=0.3, oil=2.2, wct=3.2, liquid=7.3)

        # report 2
        report2 = Report.objects.create(name='report 2', date_start=date(2022, 11, 10), calc_time=10.51,
                                        date_fin=date(2022, 11, 12), lag=1, status=Report.STATUS_CHOICES[0])
        DataFrame.objects.create(report=report2, date=date(2022, 11, 10), water=1.1, oil=3.4, wct=4.2, liquid=6.1)
        DataFrame.objects.create(report=report2, date=date(2022, 11, 11), water=1.2, oil=3.3, wct=5.2, liquid=5.2)
        DataFrame.objects.create(report=report2, date=date(2022, 11, 12), water=1.3, oil=3.2, wct=6.2, liquid=4.3)

    def test_get_report(self):
        obj = Report.objects.all()
        resp = self.client.get(reverse('report-detail', args=[obj[0].id]))
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertTrue(resp.data['created'])
        self.assertEqual(resp.data['status'], "('completed', 'закончен')")
        self.assertEqual(len(resp.data['data_frames']), 3)
        self.assertEqual(resp.data['data_frames'][0]['date'], '2022-11-10')
        self.assertEqual(resp.data['data_frames'][0]['water'], 0.1)
        self.assertEqual(resp.data['data_frames'][0]['oil'], 2.4)
        self.assertEqual(resp.data['data_frames'][0]['liquid'], 1.1)
        self.assertEqual(resp.data['data_frames'][0]['wct'], 1.2)

    def test_list_of_reports(self):
        resp = self.client.get(reverse('report-list'))
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual(resp.data['count'], 2)
        self.assertTrue(resp.data['results'][0]['name'])
        self.assertTrue(resp.data['results'][0]['created'])
        self.assertEqual(resp.data['results'][0]['status'], "('completed', 'закончен')")
