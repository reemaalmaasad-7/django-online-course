from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from onlinecourse.models import Instructor,Course,Lesson,Question,Choice
class Command(BaseCommand):
    help='Create demo course and sample exam for screenshots'
    def handle(self,*args,**options):
        inst,_=Instructor.objects.get_or_create(name='Alex Morgan',defaults={'email':'alex@example.com'})
        course,_=Course.objects.get_or_create(name='Introduction to Django',defaults={'description':'Learn Django models, views, templates, and exam evaluation.','instructor':inst})
        Lesson.objects.get_or_create(course=course,title='Getting Started',defaults={'content':'Django is a Python web framework.','order':1})
        Lesson.objects.get_or_create(course=course,title='Models and Views',defaults={'content':'Models represent data. Views process HTTP requests.','order':2})
        for question,answers in [
          ('Which language is Django based on?', [('Python',True),('Java',False),('C++',False)]),
          ('Which file configures URL routes?', [('urls.py',True),('models.py',False),('admin.py',False)]),
          ('What maps a model to database tables?', [('ORM',True),('CSS',False),('HTTP',False)])]:
            q,_=Question.objects.get_or_create(course=course,text=question)
            for txt,correct in answers: Choice.objects.get_or_create(question=q,text=txt,defaults={'is_correct':correct})
        User=get_user_model()
        if not User.objects.filter(username='demo_admin').exists():
            User.objects.create_superuser('demo_admin','demo@example.com','DemoPass123!')
        self.stdout.write(self.style.SUCCESS('Demo ready: user demo_admin / DemoPass123! (local demo only)'))
