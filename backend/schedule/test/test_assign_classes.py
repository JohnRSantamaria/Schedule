from django.core.exceptions import ValidationError
from django.test import TestCase
from schedule.models import Teacher, Student, Aptitude, Schedule
from django.utils import timezone
from datetime import timedelta
import random

class AssignClassesTestCase(TestCase):
    def setUp(self):
        # Crear 4 profesores y 50 estudiantes con aptitudes asignadas
        self.teachers = []
        self.students = []
        self.aptitude = Aptitude.objects.create(name='Matematicas')

        # Crear 4 profesores y asignarles aptitudes
        for i in range(4):
            teacher = Teacher.objects.create(name=f'Profesor {i+1}')
            teacher.aptitudes.add(self.aptitude)
            self.teachers.append(teacher)

        # Crear 50 estudiantes y asignarles aptitudes
        for i in range(50):
            student = Student.objects.create(name=f'Estudiante {i+1}')
            student.aptitudes.add(self.aptitude)
            self.students.append(student)

    def test_no_duplicate_classes(self):
        start_date = timezone.now()  # Hoy
        end_date = start_date + timedelta(weeks=4)  # Dentro de 4 semanas

        for student in self.students:
            # Asignar una clase aleatoria para cada estudiante
            available_teachers = random.sample(self.teachers, 1)  # Selecciona un profesor aleatorio
            teacher = available_teachers[0]

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
                schedule.full_clean()  # Esto validará que no haya solapamientos
                schedule.save()
            except ValidationError as e:
                # Verificar que se haya lanzado la excepción cuando hay solapamientos
                if "ya tiene una clase programada en este horario" not in str(e):
                    self.fail(f"No se pudo asignar la clase para {teacher.name} con {student.name} a las {start_time}: {e}")

        # Verificar que no haya solapamientos entre clases de profesores y estudiantes
        for teacher in self.teachers:
            for student in self.students:
                # Buscar clases asignadas a este profesor y estudiante
                schedules = Schedule.objects.filter(teacher=teacher, student=student)
                for schedule in schedules:
                    overlapping_teacher_classes = Schedule.objects.filter(
                        teacher=teacher,
                        start_time__lt=schedule.end_time,
                        end_time__gt=schedule.start_time
                    ).exclude(id=schedule.id)
                    overlapping_student_classes = Schedule.objects.filter(
                        student=student,
                        start_time__lt=schedule.end_time,
                        end_time__gt=schedule.start_time
                    ).exclude(id=schedule.id)

                    # Si hay solapamientos, lanzar error
                    if overlapping_teacher_classes.exists() or overlapping_student_classes.exists():
                        self.fail(f"Clase duplicada detectada para {teacher.name} con {student.name} a las {schedule.start_time}")
