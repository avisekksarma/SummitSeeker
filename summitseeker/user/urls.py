from django.urls import path
from . import views

urlpatterns = [
    # path('',views.UserList.as_view(),name='user-list'),
    # path('<int:pk>',views.UserDetail.as_view(),name='user-detail'),
    path('profile/',views.Profile.as_view(),name='user-profile'),
    path('register/',views.UserRegister.as_view(),name='user-register'),
    path('login/',views.UserLogin.as_view(),name='user-login'),
    path('hello/',views.Hello.as_view(),name='user-hello'),
]
