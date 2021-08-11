from django.urls import path
from . import views
from registerapp.views import UserLogin,Register
app_name = 'reg'
urlpatterns = [
    path('regs/', Register.as_view()),
    #path('login/', UserLogin.as_view()),
    #path('userAuth/', views.RegisrationionUserModel),
    #path('validUser/', views.ValidUser)
]