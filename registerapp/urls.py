from django.urls import path

from registerapp.views import Registration, UserLogin, VerifyUser

app_name = 'reg'
urlpatterns = [
    path('userReg/', Registration.as_view()),
    path('login/', UserLogin.as_view()),
    path('<str:token>/', VerifyUser.as_view())
]
