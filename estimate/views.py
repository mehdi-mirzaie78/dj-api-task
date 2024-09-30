from rest_framework import generics
from user.permissions import IsSuperUser
from .models import Estimate
from .serializers import EstimateSerializer


class EstimateListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSuperUser]
    queryset = Estimate.objects.prefetch_related("estimateequipment_set").all()
    serializer_class = EstimateSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class EstimateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperUser]
    queryset = Estimate.objects.prefetch_related("estimateequipment_set").all()
    serializer_class = EstimateSerializer
