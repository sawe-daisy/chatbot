from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
from .views import RegisterUser, edit, searchprofile

# aplication = ProtocolTypeRouter({
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(

#         )
#     )
# })

urlpatterns = [
    path('', edit, name="index"),
    path('register/', RegisterUser, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('search/', searchprofile, name='search'),
]