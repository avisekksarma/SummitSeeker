from django.urls import path
from . import views

urlpatterns = [
    path('',views.TrailListView.as_view(),name='trail-list'),
    path('<int:pk>/',views.TrailDetailView.as_view(),name='trail-detail'),
    path('<int:trail_id>/guides/',views.GuidesOnTrail.as_view(),name='guides-on-a-trail'),
    path('<int:trail_id>/guides/<int:guide_id>/hire',views.Hire.as_view(),name='hire-guide-on-a-trail'),
]
         
    