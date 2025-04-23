from rest_framework import generics
from .models import Teacher,Student,Schedule
from .serializers import TeacherSerializer, StudentSerializer, ScheduleSerializer


class TeacherCreateView(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ScheduleCreateView(generics.CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = StudentSerializer

class ScheduleListView(generics.ListAPIView):
    queryset= Schedule.objects.all()
    serializer_class = ScheduleSerializer
    