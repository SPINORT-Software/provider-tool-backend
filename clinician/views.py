from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
import datetime
from rest_framework.response import Response


class Workload:
    class WorkloadListCreateView(generics.ListCreateAPIView):
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkLoadSerialzer

    class WorkloadUpdateDeleteRetrieve(generics.RetrieveUpdateDestroyAPIView):
        """
        Retrieve, Update and Delete workload.
        """
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkLoadSerialzer

        def update(self, request, *args, **kwargs):
            existing_clinician = str(super().get_object().clinician.clinician_id)

            if request.data['clinician'] == existing_clinician:
                request.data['revision_date'] = datetime.date.today().strftime('%Y-%m-%d')
                response_workload = super().update(request, *args, **kwargs)

                return Response({
                    'status': 200,
                    'data': response_workload.data
                })
            else:
                return Response({
                    'status': 400,
                    'data': 'Failed to update the workload information. Incorrect Clinician value provided.'
                })

    class ClinicianWorkloadList(generics.ListAPIView):
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkLoadSerialzer

        def list(self, request, *args, **kwargs):
            clinician_id = kwargs.get('clinician')
            workload_objects = DailyWorkLoad.objects.filter(clinician=clinician_id)

            return Response({
                'status': 200,
                'data': DailyWorkLoadSerialzer(workload_objects, many=True).data
            })

# class InterventionsViews:
#     class WorkloadListCreateView(generics.ListCreateAPIView):
#         queryset = DailyWorkLoad.objects.all()
#         serializer_class = DailyWorkLoadSerialzer
