from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name="index"),
    path('logout', views.logout, name="logout"),
    path('register', views.register, name="register"),



    path('frontpage', views.frontpage, name="frontpage"),
    path('new_pana', views.pana, name="pana"),
    path('likethis', views.likethis, name="likethis"),
    path('likethiss', views.likethiss, name="likethiss"),
    path('likethissinprofile/<user>', views.likethissinprofile, name="likethissinprofile"),
    path('pana_details/<post_id>', views.pana_details, name="pana_details"),
    path('profile/<user>', views.profile, name="profile"),
    path('follow', views.follow, name="follow"),

    
    path('setting', views.setting, name="setting"),
]
