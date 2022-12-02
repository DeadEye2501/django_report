from django.db import models
from datetime import datetime


class Report(models.Model):
    class Meta:
        verbose_name = 'Расчет'
        verbose_name_plural = 'Расчеты'

    STATUS_CHOICES = [
        ('completed', 'закончен'),
        ('in progress', 'выполняется'),
        ('in queue', 'в очереди')
    ]

    name = models.CharField(max_length=100, default=f'new_report', verbose_name='название')
    created = models.DateTimeField(auto_now_add=True, verbose_name='расчет запрошен')
    calc_time = models.FloatField(null=True, blank=True, verbose_name='время расчета')
    date_start = models.DateField(verbose_name='дата начала')
    date_fin = models.DateField(verbose_name='дата окончания')
    lag = models.IntegerField(verbose_name='переодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[2], verbose_name='статус')

    def __str__(self):
        return f'{self.date_start}-{self.date_fin}-{self.lag}: {self.created}'

    def save(self, *args, **kwargs):
        self.name = f'report {datetime.now()}'
        super().save(*args, **kwargs)


class DataFrame(models.Model):
    class Meta:
        verbose_name = 'Данные расчета'
        verbose_name_plural = 'Данные расчетов'

    report = models.ForeignKey(to=Report, on_delete=models.CASCADE, related_name='data_frames', verbose_name='расчет')
    date = models.DateField(verbose_name='дата')
    liquid = models.FloatField(verbose_name='жидкость')
    oil = models.FloatField(verbose_name='нефть')
    water = models.FloatField(verbose_name='вода')
    wct = models.FloatField(verbose_name='обводненность')

    def __str__(self):
        return f'{self.report}: {self.date}'
