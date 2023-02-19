from django.urls import path
from . import views

urlpatterns = [
   path('',views.fillData),
   path('all/',views.TravelAgencyList.as_view(),name='agencies-list')  
]
