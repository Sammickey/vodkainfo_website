from django.urls import path, include

from . import views

urlpatterns = [
    # not include rest_framework.urls
    # which include api-auth/login on success redirect to accounts/profile/ can change with LOGIN_REDIRECT_URL = '/your/custom/path/' settings
    # & api-auth/logout views
    path('', include('rest_framework.urls'), name='rest_framework'),
    path('user_register/', views.register_view, name='user_register'),
    path('user_login/', views.login_view, name='user_login'),
]