from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "new-chat/",
        views.new_chat,
        name="new_chat"
    ),

    path(
        "chat/<int:session_id>/",
        views.chat_session,
        name="chat_session"
    ),

    path(
        "api/chat/",
        views.chat,
        name="chat_api"
    ),

    path(
        "pdf/upload/",
        views.upload_pdf,
        name="upload_pdf"
    ),

    path(
        "pdf/<int:pdf_id>/",
        views.pdf_detail,
        name="pdf_detail"
    ),
    

]