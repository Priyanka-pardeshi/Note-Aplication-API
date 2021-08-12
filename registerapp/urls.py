from django.urls import path
from . import views
from registerapp.views import RegisterLogin, Register, UserRegistrationModel,UserLogin
app_name = 'reg'
urlpatterns = [
    path('reg/', Register.as_view()),
    path('login/', RegisterLogin.as_view()),
    path('userReg/', UserRegistrationModel.as_view()),
    path('userLogin/', views.UserLogin.as_view())
]