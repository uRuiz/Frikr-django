from django.conf.urls import url

from users.api import UserListAPI
from users.views import LogoutView, LoginView

urlpatterns = [
    # Web URLs
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),

    # API URLs
    url(r'^api/1.0/users/', UserListAPI.as_view(), name='api_user_list'),
]
