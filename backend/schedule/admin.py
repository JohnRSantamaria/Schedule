from django.contrib import admin
from .models import Teacher, Student, Aptitude, Schedule

@admin.register(Aptitude)
class AptitudeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    filter_horizontal = ('aptitudes',)  

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'student', 'start_time', 'end_time')
    list_filter = ('teacher', 'student', 'start_time')
    search_fields = ('teacher__name', 'student__name')
