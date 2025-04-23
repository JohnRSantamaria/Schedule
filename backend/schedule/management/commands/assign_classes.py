from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from schedule.models import Teacher, Student, Aptitude, Schedule
from datetime import timedelta
from django.utils import timezone
import random


class Command(BaseCommand):
    help = "Asigna clases a estudiantes según las aptitudes de los profesores"

    def handle(self, *args, **kwargs):
        teachers = Teacher.objects.all()
        students = Student.objects.all()

        start_date = timezone.now()  # Hoy
        end_date = start_date + timedelta(weeks=4)  # Dentro de 4 semanas

        for student in students:            
            student_aptitudes = Aptitude.objects.filter(students=student) # Asume que tienes alguna relación para obtener las aptitudes del estudiante

            for aptitude in student_aptitudes:
                available_teachers = Teacher.objects.filter(aptitudes=aptitude)  # Buscar profesores con esa aptitud

                for teacher in available_teachers:
                    # Generar horarios aleatorios dentro de un rango
                    start_time = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
                    start_time = start_time.replace(hour=random.randint(8, 17), minute=0)

                    # Definir la hora de fin (duración de 1 hora por clase)
                    end_time = start_time + timedelta(hours=1)

                    # Crear el horario
                    schedule = Schedule(
                        teacher=teacher,
                        student=student,
                        start_time=start_time,
                        end_time=end_time
                    )

                    try:
                        # Intentar validar el horario y guardarlo
                        schedule.full_clean()  # Llama a la validación personalizada
                        schedule.save()
                        print(f"Clase asignada: {teacher.name} con {student.name} a las {start_time}")
                    except ValidationError as e:
                        print(f"No se pudo asignar la clase para {teacher.name} con {student.name} a las {start_time}: {e}")
