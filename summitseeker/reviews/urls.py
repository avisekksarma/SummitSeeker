from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_my_reviews,name='get-my-reviews'),
    path('guide/<int:pk>/',views.manage_guide_review),
    # TODO: may be see below ' have i reviewed ' api design and try to improve someway.
    # Maybe check additionally if you (tourist) went to that guide in a trail i.e. booking confirmed,
    # and then reviewed or not.
    path('guide/<int:pk>/review/check/',views.have_i_reviewed,name='have-i-reviewed'),
    path('trail/<int:trail_id>/',views.trail_reviews,name='trail-reviews')
]