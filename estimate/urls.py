from django.urls import path
from .views import EstimateListCreateView, EstimateRetrieveUpdateDestroyView

urlpatterns = [
    path('estimates/', EstimateListCreateView.as_view(), name='list-create-estimate'),
    path('estimates/<int:pk>/', EstimateRetrieveUpdateDestroyView.as_view(), name='estimate-detail'),
]