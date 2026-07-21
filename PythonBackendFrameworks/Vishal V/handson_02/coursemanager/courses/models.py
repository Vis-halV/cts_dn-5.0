from django.db import models

class Department(models.Model):

    """ IMPORTANT:
    on_delete=CASCADE on related models means deleting a
    Department also deletes its Courses and Students.
    Use on_delete=PROTECT if you want to prevent that.
    """
    
    name         = models.CharField(max_length=100)
    head_of_dept = models.CharField(max_length=100, blank=True)
    budget       = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Course(models.Model):
    name       = models.CharField(max_length=100)
    code       = models.CharField(max_length=20, unique=True)   
    credits    = models.IntegerField(default=3)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,    # deleting dept deletes its courses
        related_name='courses'       # dept.courses.all()
    )

    def __str__(self):
        return f"{self.code} — {self.name}"


class Student(models.Model):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(unique=True)             
    department      = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,   # deleting dept does NOT delete student
        null=True,
        blank=True,
        related_name='students'
    )
    enrollment_year = models.IntegerField(default=2024)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Enrollment(models.Model):
    student         = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course          = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrollment_date = models.DateField(auto_now_add=True)
    grade           = models.CharField(
        max_length=2,
        blank=True,
        null=True,                   # nullable — grade not assigned yet
        choices=[('A','A'), ('B','B'), ('C','C'), ('D','D'), ('F','F')]
    )

    # unique_together prevents the same student enrolling
    # in the same course more than once
    class Meta:
        unique_together = [['student', 'course']]

    def __str__(self):
        return f"{self.student} → {self.course} ({self.grade or 'no grade'})"
