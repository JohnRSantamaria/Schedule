from django.core.exceptions import ValidationError
from django.db import models

class Aptitude(models.Model): 
    name = models.CharField(max_length=100)

    def __str__(self): 
        return self.name 

class Teacher(models.Model): 
    name = models.CharField(max_length=100)
    aptitudes = models.ManyToManyField(Aptitude, related_name='teachers')
    

    def __str__(self): 
        return self.name    

class Student(models.Model):
    name = models.CharField(max_length=100)
    aptitudes = models.ManyToManyField(Aptitude, related_name='students')

    def __str__(self) -> str:
        return self.name
    
class Schedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        unique_together = ('teacher', 'start_time', 'student')

    def __str__(self):
        return f"{self.teacher.name} - {self.student.name} at {self.start_time}"

    def clean(self):
        # Verificar si el profesor ya tiene una clase en el mismo horario
        overlapping_teacher_classes = Schedule.objects.filter(
            teacher=self.teacher,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        
        if overlapping_teacher_classes.exists():
            raise ValidationError(f"El profesor {self.teacher.name} ya tiene una clase programada en este horario.")

        # Verificar si el estudiante ya tiene una clase en el mismo horario
        overlapping_student_classes = Schedule.objects.filter(
            student=self.student,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        
        if overlapping_student_classes.exists():
            raise ValidationError(f"El estudiante {self.student.name} ya tiene una clase programada en este horario.")

    
    

    
