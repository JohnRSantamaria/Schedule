from rest_framework import serializers
from .models import Teacher, Student, Schedule, Aptitude

class AptitudeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Aptitude
        fields = ["id",'name']

class TeacherSerializer(serializers.ModelSerializer):
    aptitudes = AptitudeSerializer(many=True)

    class Meta: 
        model = Teacher
        fields = ['id', 'name', 'aptitudes']

class StudentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Student
        fields = ['id', 'name']

class ScheduleSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Schedule
        fields = ['teacher','student','start_time','end_time']
        