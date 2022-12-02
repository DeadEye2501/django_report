from rest_framework import serializers
from django.core.exceptions import BadRequest
from .models import Report, DataFrame


class GetDataFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFrame
        fields = ('date', 'liquid', 'oil', 'water', 'wct')


class CreateDataFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFrame
        fields = ('report', 'date', 'liquid', 'oil', 'water', 'wct')

    @classmethod
    def echo(cls):
        print('echo')


class GetReportSerializer(serializers.ModelSerializer):
    OPTIONAL_FIELDS = ('name', 'calc_time')
    data_frames = GetDataFrameSerializer(many=True)

    class Meta:
        model = Report

    def __init__(self, *args, fields=None, **kwargs):
        if fields:
            add_fields = []
            for field in fields:
                if field in self.OPTIONAL_FIELDS:
                    add_fields.append(field)
                else:
                    raise BadRequest('Invalid field value')
            self.Meta.fields = ('created', 'status', 'data_frames', *add_fields)
        else:
            self.Meta.fields = ('created', 'status', 'data_frames')
        super().__init__(*args, **kwargs)


class CreateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('date_start', 'date_fin', 'lag')


class GetReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('name', 'created', 'status')
