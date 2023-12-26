from django.db import models
from accounts.models import *
# Create your models here.


class TrainingProvider(models.Model):
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255) # company name

    def __str__(self):
        return self.name


class Course(models.Model):
    COURSE_PERIODS = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
    )

    provider = models.ForeignKey(TrainingProvider, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    brief = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    period = models.CharField(max_length=255, choices=COURSE_PERIODS)
    available = models.BooleanField(default=False, null=True)
    max_student_numbers = models.IntegerField(null=True, default=100)


    @property
    def get_course_registered_students(self):
        course_register_details = self.usercourse_set.all()
        registered_students = course_register_details.count()
        return registered_students

    @property
    def get_course_seats_left(self):
        course_register_details = self.usercourse_set.all()
        registered_students = course_register_details.count()
        seats_left = self.max_student_numbers - registered_students
        if seats_left == 0:
            self.available = False

        return seats_left

    def __str__(self):
        return self.name


class UserCourse(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    course_pass = models.BooleanField(default=None, null=True, blank=True)

    def __str__(self):
        return f"[ Course: {self.course.name} ] [ Username: {self.user.username} ] [ Pass Status: {self.course_pass} ]"