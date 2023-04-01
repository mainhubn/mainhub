from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('profile_list/',views.profile_list,name='profile_list'),
    path('profile/<int:pk>/',views.profile,name='profile'),
    path('login/', views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('update_user/',views.update_user,name='update_user'),
    path('<str:room_name>/<str:username>/',views.MessageView,name='room'),
    path('Homepage/',views.hHomepage,name='hHomepage'),
    path('user_sb/',views.user_sb,name='user_sb'),
]