from .serializers import *
from rest_framework import status, generics, response


class WorkloadList(generics.ListCreateAPIView):
    """
    List all workload, or create a new daily workload.
    """
    queryset = DailyWorkLoad.objects.all()
    serializer_class = DailyWorkloadSerializer


class WorkloadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Add a workload, update a workload detail, delete a workload
    """
    queryset = DailyWorkLoad.objects.all()
    serializer_class = DailyWorkloadSerializer
