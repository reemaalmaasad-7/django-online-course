
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Course, Enrollment, Question, Choice, Submission


def course_index(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse/course_index.html', {
        'courses': courses
    })


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    questions = course.questions.prefetch_related('choices')

    return render(request, 'onlinecourse/course_details_bootstrap.html', {
        'course': course,
        'questions': questions,
    })


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    questions = list(
        course.questions.prefetch_related('choices')
    )

    if not questions:
        return HttpResponseBadRequest(
            'No exam questions configured'
        )

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    selected_ids = []

    for question in questions:
        choice_id = request.POST.get(
            f'choice_{question.pk}'
        )

        if choice_id:
            choice = Choice.objects.filter(
                pk=choice_id,
                question=question
            ).first()

            if choice:
                selected_ids.append(choice.pk)

    total = sum(
        question.grade for question in questions
    )

    score = sum(
        question.grade
        for question in questions
        if question.is_get_score(selected_ids)
    )

    submission = Submission.objects.create(
        enrollment=enrollment,
        user=request.user,
        course=course,
        score=score,
        total=total
    )

    selected_choices = Choice.objects.filter(
        pk__in=selected_ids
    )

    submission.choices.set(selected_choices)
    submission.selected_choices.set(selected_choices)

    return redirect(
        'show_exam_result',
        course_id=course.pk,
        submission_id=submission.pk
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(
        Course,
        pk=course_id
    )

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__user=request.user,
        enrollment__course=course
    )

    selected_ids = list(
        submission.choices.values_list(
            'id',
            flat=True
        )
    )

    questions = course.questions.prefetch_related('choices')

    total_grade = sum(
        question.grade for question in questions
    )

    total_score = sum(
        question.grade
        for question in questions
        if question.is_get_score(selected_ids)
    )

    grade = round(
        100 * total_score / total_grade
    ) if total_grade else 0

    items = []

    for question in questions:
        picked = [
            choice
            for choice in question.choices.all()
            if choice.id in selected_ids
        ]

        correct = [
            choice
            for choice in question.choices.all()
            if choice.is_correct
        ]

        items.append({
            'question': question,
            'chosen': picked[0] if picked else None,
            'correct': correct[0] if correct else None,
            'is_correct': question.is_get_score(
                selected_ids
            ),
        })

    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'grade': grade,
        'total_score': total_score,
        'total_grade': total_grade,
        'items': items,
        'passed': grade >= 70,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
