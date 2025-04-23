from django.urls import path
from .views import TeacherCreateView, StudentCreateView, ScheduleCreateView, ScheduleListView

urlpatterns = [
    path('teachers/', TeacherCreateView.as_view(), name='teacher-create'),
    path('students/', StudentCreateView.as_view(), name='student-create'),
    path('schedules/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/list/', ScheduleListView.as_view(), name='schedule-list'),
]
