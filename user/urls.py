from django.urls import path
from user import views

urlpatterns = [
    path('user/register/', views.Register.as_view()),
    path('user/login/', views.Login.as_view()),
    path('user/logout/', views.Logout.as_view()),
    path('user/image/add/', views.AddImage.as_view()),
    path("leader/login/", views.LeaderLogin.as_view()),
    path("leader/logout/", views.LeaderLogout.as_view()),
    path("leader/user/list/", views.GetUserList.as_view()),
    path("leader/user/images/<int:pk>/", views.GetUserImages.as_view()),
    path("leader/image/list/", views.GetImageList.as_view()),
]
