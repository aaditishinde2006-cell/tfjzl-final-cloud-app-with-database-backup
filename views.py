from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Question, Choice, Submission


@login_required
@require_POST
def submit(request):
    selected_choices = request.POST.getlist('choices')

    submission = Submission.objects.create(
        user=request.user,
        score=0
    )

    score = 0

    for choice_id in selected_choices:
        choice = get_object_or_404(Choice, id=choice_id)
        submission.choices.add(choice)

        if choice.is_correct:
            score += 1

    submission.score = score
    submission.save()

    return redirect('show_exam_result', submission_id=submission.id)


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        user=request.user
    )

    total_questions = submission.choices.count()

    context = {
        'submission': submission,
        'score': submission.score,
        'total_questions': total_questions,
        'percentage': (
            (submission.score / total_questions) * 100
            if total_questions > 0 else 0
        ),
    }

    return render(request, 'onlinecourse/exam_result.html', context)
