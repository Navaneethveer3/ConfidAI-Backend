from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Question, UserResponse, InterviewSession, Answer
import random
import cv2
import json
import base64
import numpy as np
from .facial_analysis import analyze_frame
from .utils import analyze_facial_expression
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io,logging
import traceback
from collections import Counter
from firebase_admin import auth



@csrf_exempt
def get_questions(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # Parsing the incoming request data
        data = json.loads(request.body)
        interview_stage = data.get("interview_stage", "fixed")
        skills = data.get("skills", [])
        projects = data.get("projects", [])

        questions = []

        # **Step 1: First 3 General Questions**
        if interview_stage == "fixed":
            questions = [
                {"text": "Tell me about yourself?", "type": "general"},
                {"text": "What is your passion towards your goal?", "type": "general"},
                {"text": "What are your skills?", "type": "general"},
            ]
            # Returning questions and transitioning to "skills" stage
            return JsonResponse({"questions": questions, "interview_stage": "skills"})

        # **Step 2: Fetch Skill-Based Questions**
        elif interview_stage == "skills":
            if not skills:
                return JsonResponse({"error": "No skills provided"}, status=400)

            # Fetch questions based on all provided skills and randomize them
            skill_based_questions = []
            for skill in skills:
                skill_questions = list(Question.objects.filter(type="skill", skill=skill).values("text", "type"))
                skill_based_questions.extend(skill_questions)

            if not skill_based_questions:
                return JsonResponse({"error": "No questions found for the provided skills"}, status=404)

            # Randomly pick 6 questions from the combined pool of questions for the skills provided
            random.shuffle(skill_based_questions)  # Shuffle the list to randomize
            questions = skill_based_questions[:6]

            # After skill questions, transition to "projects" stage
            return JsonResponse({"questions": questions, "interview_stage": "projects"})

        # **Step 3: Ask if user has projects**
        elif interview_stage == "projects":
            if not projects:
                # If no projects, end the interview
                return JsonResponse({"questions": [], "interview_stage": "end", "message": "No projects provided. Interview ended."})

            # If there are projects, generate dynamic project questions
            dynamic_project_questions = generate_project_questions(projects)
            return JsonResponse({"questions": dynamic_project_questions, "interview_stage": "end"})

        # **Step 4: End Interview**
        elif interview_stage == "end":
            return JsonResponse({"message": "Interview completed. Generating report."})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Something went wrong"}, status=500)


# Function to generate dynamic project-based questions (You can customize it based on your needs)
def generate_project_questions(projects):
    project_questions = []
    for project in projects:
        project_questions.append({
            "text": f"Tell me about the {project} project.",
            "type": "project"
        })
        project_questions.append({
            "text": f"What challenges did you face while working on the {project} project?",
            "type": "project"
        })
        project_questions.append({
            "text": f"How did you overcome the challenges in the {project} project?",
            "type": "project"
        })
    return project_questions


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")


@csrf_exempt
def analyze_webcam(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        frame = request.FILES.get("frame")
        if not frame:
            return JsonResponse({"error": "No frame received"}, status=400)

        nparr = np.frombuffer(frame.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        confidence = np.random.randint(40, 90)  # Simulating confidence analysis

        return JsonResponse({"confidence_level": confidence})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def generate_project_questions(projects):
    """Dynamically generate project-based questions."""
    questions = []
    for project in projects:
        questions.append({"text": f"Can you explain the working of your project ?", "type": "project"})
        questions.append({"text": f"What challenges did you face in your project?", "type": "project"})
        questions.append({"text": f"What technologies did you use in your projects?", "type": "project"})
        questions.append({"text": f"How did you test and debug in your projects?", "type": "project"})
        questions.append({"text": f"What improvements can be made in your projects?", "type": "project"})
        questions.append({"text": f"How does it differ from similar projects?", "type": "project"})

    return questions[:6]


# Webcam facial analysis
@csrf_exempt
def analyze_webcam_feed(request):
    if request.method == "POST":
        try:
            # Load JSON data from request
            data = json.loads(request.body.decode("utf-8"))

            # Extract Base64 image
            image_data = data.get("image")
            if not image_data:
                return JsonResponse({"error": "No image provided"}, status=400)

            # Decode Base64 image
            image_data = image_data.split(",")[1]  # Remove 'data:image/jpeg;base64,' prefix
            decoded_img = base64.b64decode(image_data)
            np_arr = np.frombuffer(decoded_img, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if img is None:
                return JsonResponse({"error": "Invalid image"}, status=400)

            # Convert image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect face
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

            if len(faces) == 0:
                return JsonResponse({"confidence_level": 0, "message": "No face detected"})

            # Process first detected face
            (x, y, w, h) = faces[0]
            face_roi = gray[y:y + h, x:x + w]

            # Detect eyes within face
            eyes = eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15))

            # Detect mouth within face
            mouth = mouth_cascade.detectMultiScale(face_roi, scaleFactor=1.5, minNeighbors=15, minSize=(30, 30))

            # Calculate Confidence Score
            confidence_level = calculate_confidence(len(eyes), len(mouth))
            session_confidence_levels = request.session.get("confidence_levels", [])
            session_confidence_levels.append(confidence_level)
            request.session["confidence_levels"] = session_confidence_levels
            return JsonResponse({"confidence_level": confidence_level})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Function to calculate confidence based on detected features
def calculate_confidence(eyes_detected, mouth_detected):
    """
    Calculate a confidence level based on detected facial features.
    The logic below is simple, but can be adjusted for your application.
    """
    if eyes_detected > 0 and mouth_detected > 0:
        # High confidence if both eyes and mouth are detected
        return random.randint(70,90)
    elif eyes_detected > 0:
        # Medium confidence if only eyes are detected
        return random.randint(40,70)
    elif mouth_detected > 0:
        # Low confidence if only mouth is detected
        return random.randint(20,40)
    else:
        # No facial features detected, very low confidence
        return random.randint(0,20)

from .serializers import InterviewSessionSerializer
from django.utils.timezone import now

@api_view(["POST"])
def create_session(request):
    user_id = request.data.get("user_id")

    if not user_id:
        return JsonResponse({"error": "User ID is required"}, status=400)

    # ✅ Check if an active session exists WITH ANSWERS
    active_session = InterviewSession.objects.filter(user_id=user_id, completed_at=None).first()

    if active_session:
        from .models import Answer
        has_answers = Answer.objects.filter(session=active_session).exists()

        if has_answers:  # ✅ Return only if session has answers
            return JsonResponse({"session_id": active_session.id}, status=200)

    # ✅ Create a new session if none exists or if the existing one has no answers
    new_session = InterviewSession.objects.create(user_id=user_id, started_at=now())
    return JsonResponse({"session_id": new_session.id}, status=201)





# Storing answers submitted by users
@api_view(['POST'])
def store_answer(request):
    if request.method == "POST":
        user_id = request.data.get("user_id")  # Use request.data
        session_id = request.data.get("session_id")  # Use request.data
        question = request.data.get("question")
        answer = request.data.get("answer")
        confidence_level = request.data.get("confidence_level", 0.0)

        if not user_id or not session_id:
            return JsonResponse({"error": "User ID and Session ID are required"}, status=400)

        # Get the session safely
        session = InterviewSession.objects.filter(id=session_id, user_id=user_id).first()
        if not session:
            return JsonResponse({"error": "Session not found"}, status=404)

        # Save the answer
        Answer.objects.create(
            session=session,
            question=question,
            answer=answer,
            confidence_level=confidence_level
        )

        return JsonResponse({"message": "Answer stored successfully"}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)




logger = logging.getLogger(__name__)




def analyze_realtime_performance():
    # Simulate confidence levels across the interview (Replace with actual OpenCV-based analysis)
    confidence_levels = [random.randint(50, 80) for _ in range(10)]  
    overall_confidence = round(sum(confidence_levels) / len(confidence_levels), 2)  # Calculate average confidence

    # Simulated facial expression analysis (Replace with actual OpenCV logic)
    facial_expressions = {
        "happy": f"{random.randint(40, 70)}%",
        "neutral": f"{random.randint(20, 50)}%",
        "sad": f"{random.randint(5, 20)}%",
    }

    return overall_confidence, facial_expressions

# ✅ AI-based overall feedback generator
def generate_overall_feedback(confidence, expressions):
    if confidence < 50:
        return "Your confidence is low. Practice speaking clearly and with more enthusiasm to improve your delivery."
    elif 50 <= confidence < 70:
        return "You're doing well, but adding more energy and engagement can make your responses stronger."
    else:
        return "Great job! You displayed strong confidence. Keep refining your communication skills for even better results."

# ✅ Real-time Report Generation API
@api_view(['GET'])
def generate_report(request, user_id):
    try:
        print(f"🔍 Generating real-time report for user: {user_id}")

        # ✅ Get real-time analysis
        overall_confidence, facial_expressions = analyze_realtime_performance()

        # ✅ Generate overall feedback dynamically
        overall_feedback = generate_overall_feedback(overall_confidence, facial_expressions)

        # ✅ Generate report data dynamically
        report_data = {
            "user_id": user_id,
            "average_confidence_level": overall_confidence,
            "facial_expressions": facial_expressions,
            "overall_improvement_suggestion": overall_feedback,
            "session_started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "session_completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        print(f"✅ Real-time report generated successfully for user {user_id}")
        return Response(report_data, status=200)

    except Exception as e:
        print(f"❌ Backend Error: {str(e)}")
        return Response({"error": "An error occurred while generating the real-time report.", "details": str(e)}, status=500)







# Analyzing facial expression
@api_view(['POST'])
def analyze_expression(request):
    try:
        frame = request.FILES['frame']
        image = Image.open(frame)
        image = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load OpenCV face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))

        if len(faces) == 0:
            return Response({"confidence": 50})  # Default confidence when no face detected

        # If face detected, analyze expression (simplified logic)
        confidence_level = np.random.randint(60, 100)  # Simulated confidence value for now

        return Response({"confidence": confidence_level})
    
    except Exception as e:
        print(f"Error analyzing expression: {e}")
        return Response({"confidence": 50})  # Default confidence level


# Get user's past interview sessions
@api_view(['POST'])
def get_interview_sessions(request):
    """
    Get past interview history for a user.
    """
    try:
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)

        interviews = InterviewResponse.objects.filter(user_id=user_id).values("timestamp").distinct()
        
        interview_sessions = []
        for interview in interviews:
            session_time = interview["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            interview_sessions.append(session_time)

        return Response({"sessions": interview_sessions})

    except Exception as e:
        return Response({"error": f"Internal Server Error: {str(e)}"}, status=500)


# Generate PDF report for the interview
@api_view(['POST'])
def generate_pdf_report(request):
    try:
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)

        responses = UserResponse.objects.filter(user_id=user_id)

        if not responses.exists():
            return Response({"error": "No responses found"}, status=404)

        # Create PDF buffer
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("Interview Report")

        # Title
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 750, "Interview Performance Report")

        # User Info
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 720, f"User ID: {user_id}")
        pdf.drawString(100, 700, f"Total Questions Answered: {responses.count()}")

        y_position = 680

        # Iterate over user responses
        for response in responses:
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(100, y_position, f"Q: {response.question}")

            y_position -= 20
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, y_position, f"A: {response.answer}")

            y_position -= 20
            pdf.drawString(100, y_position, f"Confidence Level: {response.confidence_level}%")

            if response.facial_expression:
                y_position -= 20
                pdf.drawString(100, y_position, f"Facial Expression: {response.facial_expression}")

            y_position -= 20
            pdf.drawString(100, y_position, f"Timestamp: {response.timestamp}")

            y_position -= 40  # Space between responses

            if y_position < 100:  # Avoid overflow
                pdf.showPage()
                y_position = 750

        # Save and return PDF
        pdf.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Interview_Report.pdf"'
        return response

    except Exception as e:
        return Response({"error": f"Internal Server Error: {str(e)}"}, status=500)
