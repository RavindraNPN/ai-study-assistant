from django.urls import path
from . import views

app_name = "exam"

urlpatterns = [
    path("", views.mock_test_list, name="mock_test_list"),

    path(
        "<int:test_id>/",
        views.mock_test_detail,
        name="mock_test_detail"
    ),

    path(
        "<int:test_id>/start/",
        views.start_test,
        name="start_test"
    ),

    path(
        "attempt/<int:attempt_id>/",
        views.take_test,
        name="take_test"
    ),

    path(
        "attempt/<int:attempt_id>/submit/",
        views.submit_test,
        name="submit_test"
    ),

    path(
        "attempt/<int:attempt_id>/result/",
        views.test_result,
        name="test_result"
    ),
]