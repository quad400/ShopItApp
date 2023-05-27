from django.urls import path

from .views import user_update,user_profile

urlpatterns = [
 
    path('userprofile', user_profile, name='user_profile'),
    path('userupdate', user_update, name='user_update'),   
]