from django.urls import path
from . import views

urlpatterns = [
    # path('',views.UserList.as_view(),name='user-list'),
    # path('<int:pk>',views.UserDetail.as_view(),name='user-detail'),
    path('user/<int:user_id>',views.UserDetail.as_view(),name='user-detail'),
    path('user/profile/',views.Profile.as_view(),name='user-profile'),
    path('user/register/',views.UserRegister.as_view(),name='user-register'),
    path('user/login/',views.UserLogin.as_view(),name='user-login'),
    path('user/hello/',views.Hello.as_view(),name='user-hello'),
    path('languages/',views.LanguageManager.as_view(),name='languages'),
    path('countries/',views.CountriesList.as_view(),name='countries'),
    path('user/notifications/',views.Notification.as_view(),name='notification'),
    path('user/cancelrequest/<int:hire_id>',views.CancelRequest.as_view(),name='cancelrequest'),
    path('response/<int:hire_id>/',views.HireAcceptOrRejectView.as_view(),name='hire-response-by-guide'),
    path('hire/<int:hire_id>/',views.HireTheGuide.as_view(),name='final-hire-by-tourist'),
]
