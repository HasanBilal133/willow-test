from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import GetAccount, GetBookings, DoctorSlotsCreateList, UpdateDoctorAccount, RegisterView

urlpatterns = [
    path('account/<int:pk>', GetAccount.as_view(), name='doctor-account'),
    path('bookings/', GetBookings.as_view(), name='doctor-bookings'),
    path('slots/', DoctorSlotsCreateList.as_view(), name='doctor-slots'),
    path('account/<int:pk>/update/', UpdateDoctorAccount.as_view(), name='doctor-update'),
    path('account/register/', RegisterView.as_view(), name='doctor-register'),
    #JWT urls
    path('account/login/', obtain_jwt_token, name="login"),
]