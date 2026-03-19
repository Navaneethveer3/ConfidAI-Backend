### Confid Ai - AI Powered Smart Interview System



Confid AI Designed to simulate real interview scenarios and provide intelligent feedback to candidates. The system is built with a Django REST API Backend which is deployed on Render and a ReactJS Frontend which is deployed on Netlify, ensuring scalability and seamless integration.



##### Key Features :



* **Webcam-based Interview :** Real-time video recording using OpenCV integrated with the frontend.
* **Speech-to-text :** Converts candidate answers into text for further analysis.
* **AI-Powered Analysis :** Confidence Score, Facial Expression Analysis, Answer Accuracy.
* **Dynamic Question Flow :** Common Interview Questions, Skill-based unique questions.
* **Real-Time Metrics Display :** Candidate confidence levels shown live during interview.
* **Final Report Generation :** Overall confidence score, Facial expression trends, Answer Quality \& Accuracy, Personalized improvement suggestions.







##### Tech Stack : 



* **Frontend :** ReactJS, integrated with webcam, live metrics display and report visualization.
* **Backend :** Django REST Framework, handling API endpoints for analysis, and report generation.
* **AI/NLP :** Speech-to-Text, Emotion Detection(OpenCV), Confidence \& Accuracy analysis.
* **Database :** SQLite for temporary session data storage.







##### Deployment : 



* **Backend :** Deployed on Render with production-ready settings.
* **Frontend :** Deployed on Netlify, fetching APIs from the Render Backend.
* Communication secured via REST API calls with CORS enabled for allowed domains.







##### Impact : 



This project helps candidates practice interviews realistically and gain AI-driven feedback without needing human interviewer. It benefits many people like college students, people preparing for interviews, etc.......









###### What Problems did you face while building this project?



* **Real-time Processing.**
* **Speech-to-Text Accuracy :** to handle this, experimented with noise free audio.
* **Handling Frontend and Backend :** live accuracy testing while integrating Frontend and Backend is little headache while building this project.









###### Why did you choose this tech stack?



* **Django REST Framework :** It is reliable, secure, and fast to build REST APIs. It has built in user management and middleware support which made it easy to handle interview data.
* **ReactJS :** React is the fastest frontend framework still exists in the market. It allowed me to build an interactive, real-time UI. Handling live webcam feed, showing dynamic confidence levels and rendering reports became much easier with React's component based with minimal setup.
* **OpenCV :** It helps in improving accuracy of face emotions and confidence analysis.
