from django.conf import settings
from django.db import models

class Instructor(models.Model):
    name=models.CharField(max_length=120)
    email=models.EmailField(blank=True)
    def __str__(self): return self.name

class Course(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    instructor=models.ForeignKey(Instructor,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self): return self.name

class Enrollment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    class Meta: unique_together=('user','course')
    def __str__(self): return f'{self.user}: {self.course}'

class Lesson(models.Model):
    course=models.ForeignKey(Course,related_name='lessons',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content=models.TextField(blank=True)
    order=models.PositiveIntegerField(default=1)
    class Meta: ordering=['order','id']
    def __str__(self): return self.title

class Question(models.Model):
    course=models.ForeignKey(Course,related_name='questions',on_delete=models.CASCADE)
    text=models.CharField(max_length=500)
    def __str__(self): return self.text

class Choice(models.Model):
    question=models.ForeignKey(Question,related_name='choices',on_delete=models.CASCADE)
    text=models.CharField(max_length=300)
    is_correct=models.BooleanField(default=False)
    def __str__(self): return self.text

class Submission(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    score=models.PositiveIntegerField(default=0)
    total=models.PositiveIntegerField(default=0)
    submitted_at=models.DateTimeField(auto_now_add=True)
    selected_choices=models.ManyToManyField(Choice,blank=True)
    def __str__(self): return f'{self.user} - {self.course} ({self.score}/{self.total})'
