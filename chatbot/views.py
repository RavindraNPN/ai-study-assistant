from django.shortcuts import render, redirect

# Create your views here.
from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST

from .models import *
from .services.ai_service import ask_ai

from django.contrib import messages

from .services.pdf_service import (
    extract_text_from_pdf,
    summarize_pdf,
    ask_question_from_pdf
)

from .services.rag_service import index_pdf

@csrf_exempt
def chat(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required"
        }, status=405)

    try:
        data = json.loads(request.body)

        question = data.get("message")

        if not question:
            return JsonResponse({
                "error": "Message is required"
            }, status=400)

        answer = ask_ai(question)

        return JsonResponse({
            "answer": answer
        })

    except Exception as e:
        print("AI ERROR:", e)

        return JsonResponse({"error": "AI service is currently unavailable."}, status=500)

@login_required
@require_POST
def chat(request):

    try:

        data = json.loads(request.body)

        question = data.get("message")
        session_id = data.get("session_id")

        if not question:
            return JsonResponse({
                "error": "Message is required"
            }, status=400)

        session = ChatSession.objects.filter(
            id=session_id,
            user=request.user
        ).first()

        if not session:
            return JsonResponse({
                "error": "Chat session not found"
            }, status=404)

        # Save user message

        Message.objects.create(
            session=session,
            role="user",
            content=question
        )

        # AI

        answer = ask_ai(question)

        # Save AI response

        Message.objects.create(
            session=session,
            role="assistant",
            content=answer
        )

        return JsonResponse({
            "answer": answer
        })

    except Exception as e:

        print("AI ERROR:", e)

        return JsonResponse({
            "error": "AI service is currently unavailable."
        }, status=500)

def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("dashboard")

    else:

        form = UserCreationForm()

    return render(
        request,
        "chatbot/register.html",
        {
            "form": form
        }
    )

@login_required
def dashboard(request):

    sessions = ChatSession.objects.filter(
        user=request.user
    ).order_by("-updated_at")

    pdfs = UploadedPDF.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "chatbot/dashboard.html",
        {
            "sessions": sessions,
            "pdfs": pdfs,
        }
    )

@login_required
def new_chat(request):

    session = ChatSession.objects.create(
        user=request.user,
        title="New Chat"
    )

    return redirect(
        "chat_session",
        session_id=session.id
    )

@login_required
def chat_session(request, session_id):

    session = ChatSession.objects.filter(
        id=session_id,
        user=request.user
    ).first()

    if not session:
        return redirect("dashboard")

    messages = session.messages.all()

    return render(
        request,
        "chatbot/chat.html",
        {
            "session": session,
            "messages": messages,
        }
    )



@login_required
def upload_pdf(request):

    if request.method == "POST":

        pdf_file = request.FILES.get("file")

        if not pdf_file:
            messages.error(
                request,
                "Please select a PDF file."
            )

            return redirect("upload_pdf")

        if not pdf_file.name.lower().endswith(".pdf"):
            messages.error(
                request,
                "Only PDF files are allowed."
            )

            return redirect("upload_pdf")

        extracted_text = extract_text_from_pdf(
            pdf_file
        )

        pdf = UploadedPDF.objects.create(
            user=request.user,
            file=pdf_file,
            title=pdf_file.name,
            extracted_text=extracted_text
        )

        chunk_count = index_pdf(
            pdf.id,
            request.user.id,
            extracted_text
        )

        messages.success(
            request,
            "PDF uploaded successfully!"
        )

        return redirect(
            "pdf_detail",
            pdf_id=pdf.id
        )

    return render(
        request,
        "chatbot/upload_pdf.html"
    )

@login_required
def pdf_detail(request, pdf_id):

    pdf = UploadedPDF.objects.filter(
        id=pdf_id,
        user=request.user
    ).first()

    if not pdf:
        return redirect("dashboard")

    summary = None
    answer = None
    question = None

    chat_messages = PDFChatMessage.objects.filter(
        pdf=pdf,
        user=request.user
    )

    if request.method == "POST":

        action = request.POST.get("action")

        # =========================
        # GENERATE SUMMARY
        # =========================

        if action == "summary":

            summary = summarize_pdf(
                pdf.extracted_text
            )

        # =========================
        # ASK QUESTION
        # =========================

        elif action == "question":

            question = request.POST.get(
                "question",
                ""
            ).strip()

            if question:

                answer = ask_question_from_pdf(
                    pdf.id,
                    request.user.id,
                    question
                )

                PDFChatMessage.objects.create(
                    pdf=pdf,
                    user=request.user,
                    question=question,
                    answer=answer
                )

                chat_messages = PDFChatMessage.objects.filter(
                    pdf=pdf,
                    user=request.user
                )

    return render(
        request,
        "chatbot/pdf_detail.html",
        {
            "pdf": pdf,
            "summary": summary,
            "question": question,
            "answer": answer,
            "chat_messages": chat_messages,
        }
    )