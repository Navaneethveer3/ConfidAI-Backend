import cv2

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def analyze_facial_expression(frame):
    """
    Analyze facial expressions and confidence level using OpenCV.
    Returns a confidence score.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) > 0:
        confidence = min(100, len(faces) * 20)  # Simple logic: More faces detected = lower confidence
    else:
        confidence = 10  # If no face detected, assume low confidence

    return confidence
