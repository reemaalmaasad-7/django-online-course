from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Choice, Course, Submission

def course_index(request):
    return render(request,'onlinecourse/course_index.html',{'courses':Course.objects.all()})

def course_details(request,course_id):
    course=get_object_or_404(Course,pk=course_id)
    return render(request,'onlinecourse/course_details_bootstrap.html',{'course':course,'questions':course.questions.prefetch_related('choices')})

@login_required
@require_POST
def submit(request,course_id):
    course=get_object_or_404(Course,pk=course_id)
    questions=list(course.questions.prefetch_related('choices'))
    if not questions:
        return HttpResponseBadRequest('No exam questions are configured for this course.')
    selected=[]
    score=0
    for question in questions:
        choice_id=request.POST.get(f'question_{question.pk}')
        choice=Choice.objects.filter(pk=choice_id,question=question).first() if choice_id else None
        if choice:
            selected.append(choice)
            if choice.is_correct:
                score+=1
    submission=Submission.objects.create(user=request.user,course=course,score=score,total=len(questions))
    submission.selected_choices.set(selected)
    return redirect('show_exam_result',submission_id=submission.pk)

@login_required
def show_exam_result(request,submission_id):
    submission=get_object_or_404(Submission,pk=submission_id,user=request.user)
    selected_ids=set(submission.selected_choices.values_list('id',flat=True))
    items=[]
    for question in submission.course.questions.prefetch_related('choices'):
        chosen=next((c for c in question.choices.all() if c.pk in selected_ids),None)
        correct=next((c for c in question.choices.all() if c.is_correct),None)
        items.append({'question':question,'chosen':chosen,'correct':correct,'is_correct':chosen is not None and chosen.pk==getattr(correct,'pk',None)})
    percentage=round(submission.score/submission.total*100) if submission.total else 0
    return render(request,'onlinecourse/exam_result.html',{'submission':submission,'items':items,'percentage':percentage,'passed':percentage>=70})
