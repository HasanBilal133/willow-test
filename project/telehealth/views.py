from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import AccountSerializer, BookingsSerializer, SlotSerializer, RegisterSerializer
from .models import Doctor, Booking, Slot, Specialities


MyUser = get_user_model()

# Create your views here.
class GetAccount(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Doctor.objects.all()


class GetBookings(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingsSerializer
    def get_queryset(self):
        doctor = get_object_or_404(Doctor, user=self.request.user)
        bookings = Booking.objects.filter(doctor=doctor)
        if len(bookings) < 1:
            return HttpResponse("there isn't any booking")
        return bookings


class DoctorSlotsCreateList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SlotSerializer
    def get_queryset(self):
        doctor = get_object_or_404(Doctor, user=self.request.user)
        slots = Slot.objects.filter(doctor=doctor)
        if len(slots) < 1:
            return HttpResponse("there isn't any available slot")
        return slots
    
    def create(self, *args, **kwargs):
        doctor = get_object_or_404(Doctor, user=self.request.user)
        data_dict = self.request.POST
        slot = Slot(doctor=doctor, available_at=data_dict['available_at'])
        qs = slot.save()
        return redirect('doctor-slots')


class UpdateDoctorAccount(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = Doctor.objects.all()


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    queryset = Doctor.objects.all()
        
            
            