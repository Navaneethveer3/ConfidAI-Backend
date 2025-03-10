import cv2

# Load OpenCV's pre-trained Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def analyze_frame(frame):
    """
    Detect faces and return the confidence level (as an approximation).
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # Detect faces

    confidence_level = len(faces) * 20  # Approximate confidence level

    return confidence_level  # Return detected confidence level
