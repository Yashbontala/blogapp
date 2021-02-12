from django.urls import path
from . import views
from .views import  CreatePostView,WelcomePageView,SearchUserView
from django.conf.urls import   url
from .forms import NewUserForm

app_name = "main" 
                                                                         


urlpatterns = [
    path('welcome/', WelcomePageView.as_view(), name='welcome'),
    path("register/", views.register_request, name="register"),
    path("search/",SearchUserView.as_view(), name="search"),
    path("", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path('post/', CreatePostView.as_view(), name='add_post'),
]
