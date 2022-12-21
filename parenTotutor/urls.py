from django.urls import path
from .views import dashboard, profile_list, profile 

app_name = "parenTotutor"

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path ("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path('logout/', views.logout_view, name="logout"),

]