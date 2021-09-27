from django.urls import path

from registerapp.views import Registration, UserLogin, VerifyUser

app_name = 'reg'
urlpatterns = [
    # add name
    path('userReg/', Registration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='Login'),
    path('<str:token>/', VerifyUser.as_view(), name='verification')
]
