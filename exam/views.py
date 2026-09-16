from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    MockTest,
    StudentAttempt,
)


@login_required
def mock_test_list(request):
    tests = MockTest.objects.filter(
        is_published=True
    ).select_related("subject", "unit")

    return render(
        request,
        "exam/mock_test_list.html",
        {"tests": tests}
    )


@login_required
def mock_test_detail(request, test_id):
    test = get_object_or_404(
        MockTest.objects.select_related("subject", "unit"),
        id=test_id,
        is_published=True
    )

    questions = test.test_questions.select_related(
        "question"
    ).prefetch_related(
        "question__options"
    )

    return render(
        request,
        "exam/mock_test_detail.html",
        {
            "test": test,
            "questions": questions,
        }
    )


@login_required
def start_test(request, test_id):
    test = get_object_or_404(
        MockTest,
        id=test_id,
        is_published=True
    )

    attempt = StudentAttempt.objects.create(
        student=request.user,
        mock_test=test,
    )

    return redirect(
        "exam:take_test",
        attempt_id=attempt.id
    )


@login_required
def take_test(request, attempt_id):
    attempt = get_object_or_404(
        StudentAttempt.objects.select_related(
            "mock_test"
        ),
        id=attempt_id,
        student=request.user,
        is_completed=False,
    )

    questions = attempt.mock_test.test_questions.select_related(
        "question"
    ).prefetch_related(
        "question__options"
    )

    return render(
        request,
        "exam/take_test.html",
        {
            "attempt": attempt,
            "questions": questions,
        }
    )


@login_required
def submit_test(request, attempt_id):
    attempt = get_object_or_404(
        StudentAttempt,
        id=attempt_id,
        student=request.user,
        is_completed=False,
    )

    # Evaluation will be implemented next.
    return redirect(
        "exam:test_result",
        attempt_id=attempt.id
    )


@login_required
def test_result(request, attempt_id):
    attempt = get_object_or_404(
        StudentAttempt.objects.select_related(
            "mock_test"
        ),
        id=attempt_id,
        student=request.user,
    )

    return render(
        request,
        "exam/test_result.html",
        {
            "attempt": attempt,
        }
    )
