from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_my_reviews,name='get-my-reviews'),
    path('guide/<int:pk>/',views.get_guide_review,name='get-guide-reviews'),
    path('guide/<int:pk>/review/',views.make_guide_review,name='make-guide-review'),
    path('guide/<int:pk>/review/check',views.have_i_reviewed,name='have-i-reviewed')
]