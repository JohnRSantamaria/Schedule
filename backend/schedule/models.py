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

    def __str__(self) -> str:
        return self.name
    
class Schedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta: 
        unique_together = ('teacher', 'start_time', 'student')
    
    def __str__(self) -> str:
        return f"{self.teacher.name} - {self.student.name} at {self.start_time}"
    
    

    
