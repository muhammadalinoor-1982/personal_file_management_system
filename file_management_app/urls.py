
from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
#URL for Athentication
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('register/', register, name='register'),

#URL for E-Mail Verification
    path('success/', success, name='success'),
    path('token_send/', token_send, name='token_send'),
    path('error/', error, name='error'),
    path('verify/<auth_token>/', verify, name='verify'),

    #CRUD
    path('ex_create/', ex_create, name='ex_create'),
    path('ex_update/<id>/', ex_update, name='ex_update'),
    path('ex_delete/<id>/', ex_delete, name='ex_delete')
]
