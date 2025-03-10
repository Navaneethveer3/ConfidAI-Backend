from django.urls import path
from .views import get_questions,analyze_webcam_feed,store_answer,generate_report,analyze_expression,get_interview_sessions,generate_pdf_report
from .views import create_session

urlpatterns = [
    path('start-interview/get-questions/', get_questions, name='get_questions'),
    path("start-interview/analyze-webcam/", analyze_webcam_feed, name="analyze_webcam"),
    path("start-interview/store-answer/",store_answer,name="store-answer"),
    path('generate-report/<str:user_id>/', generate_report, name='generate-report'),
    path('start-interview/analyze-expression/',analyze_expression,name='analyze-expression'),
    path('start-interview/get-interview-sessions/',get_interview_sessions,name='get-interview-sessions'),
    path('start-interview/generate-pdf-report/',generate_pdf_report,name='generate-pdf-report'),
    path("start-interview/create-session/", create_session, name="create_session"),
]
