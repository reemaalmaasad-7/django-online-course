
from django.conf import settings
from django.db import models


class Instructor(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user}: {self.course}'


class Learner(Enrollment):
    class Meta:
        proxy = True
        verbose_name = 'Learner'
        verbose_name_plural = 'Learners'


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='lessons',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Question(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='questions',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=500)
    grade = models.PositiveIntegerField(default=1)

    def is_get_score(self, selected_ids):
        correct = set(
            self.choices.filter(
                is_correct=True
            ).values_list('id', flat=True)
        )

        selected = set(
            self.choices.filter(
                id__in=selected_ids
            ).values_list('id', flat=True)
        )

        return bool(correct) and correct == selected

    @property
    def course_name(self):
        return self.course.name

    @property
    def question_text(self):
        return self.text

    @property
    def grade_points(self):
        return self.grade

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='choices',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='submissions'
    )
    choices = models.ManyToManyField(
        Choice,
        blank=True,
        related_name='submissions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    selected_choices = models.ManyToManyField(
        Choice,
        blank=True
    )

    def __str__(self):
        return (
            f'{self.user} - {self.course} '
            f'({self.score}/{self.total})'
        )
