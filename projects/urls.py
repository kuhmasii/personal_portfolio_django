from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("about/", views.about_me, name="about_me"),
    path('projectpage/', views.project, name='project'),
    path("contact/", views.contact, name='contact'),
    path('login/', views.user_login, name="user_login"),
    path('account/', views.dashboard, name="account"),
    path("upload/", views.upload, name="upload"),
    path("update/", views.update, name="update"),
    path("logout/", views.user_logout, name='user_logout'),
]
