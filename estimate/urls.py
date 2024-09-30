from django.urls import path
from .views import EstimateListCreateView, EstimateRetrieveUpdateDestroyView

urlpatterns = [
    path("estimates/", EstimateListCreateView.as_view(), name="estimate-list-create"),
    path(
        "estimates/<int:pk>/",
        EstimateRetrieveUpdateDestroyView.as_view(),
        name="estimate-detail",
    ),
]
