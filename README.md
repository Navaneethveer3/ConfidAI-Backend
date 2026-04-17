# Confid AI — Practice Interviews Without the Pressure

## Overview

Interview anxiety is real, and most people don't get enough practice before the actual thing. Confid AI is an interview simulation platform I built to change that. It puts you through a realistic interview — webcam on, questions coming in, clock ticking — and when it's done, gives you detailed AI-driven feedback on how you actually performed.

The goal wasn't just to quiz people on answers. It was to analyze the full picture: how you spoke, how you carried yourself, and how your confidence held up under pressure.

Live demo: https://confidai.netlify.app/

---

## What It Does

- Runs a live webcam-based interview session using OpenCV integrated with the frontend
- Converts spoken responses to text for deeper analysis
- Scores confidence levels in real time during the session
- Analyzes facial expressions throughout the interview
- Evaluates answer accuracy and relevance
- Walks through a dynamic question set — common HR questions plus skill-based and adaptive ones
- Displays live metrics on a dashboard while the interview is in progress
- Generates a full report at the end covering confidence scores, expression trends, answer quality, and personalized suggestions

---

## Tech Stack

- Frontend: React.js, deployed on Netlify — handles webcam feed, live metrics, and report dashboards
- Backend: Django REST Framework on Render — processes analysis, manages sessions, and generates reports
- AI/ML: Speech-to-text processing, facial emotion detection via OpenCV, confidence and accuracy scoring
- Database: SQLite for session-based storage

---

## How It Works

1. User starts a session and the webcam activates
2. Questions are served one by one through the interface
3. Responses are captured via speech-to-text and video simultaneously
4. AI analyzes confidence, facial cues, and answer quality in real time
5. At the end, a comprehensive report is generated with scores and improvement areas

---

## Challenges Worth Mentioning

**Keeping latency low during live sessions** — processing video, audio, and metrics all at once without noticeable lag was the toughest part. Required careful optimization of how data flows between the frontend and backend during an active session.

**Speech-to-text reliability** — background noise and inconsistent microphone quality were causing noticeable accuracy drops. Spent time tuning the audio input handling to make transcription more consistent across different environments.

**Syncing everything in real time** — coordinating live video, metric updates, and API calls during an interview without things falling out of sync took a lot of iteration to get right.

---

## Why These Tools

Django REST Framework is solid for building APIs that need to handle authentication, structured data, and multiple processing steps cleanly. React's component model made it straightforward to build a UI that updates in real time without re-rendering everything. OpenCV was the practical choice for facial detection — it's well-documented, reliable, and integrates well with Python-based backends.

---

## Who It's Built For

- Students getting ready for campus placements
- Job seekers who want honest, structured feedback before the real interview
- Professionals looking to sharpen how they communicate under pressure

---

## What's Next

- Stronger NLP-based evaluation of answer quality and depth
- Multilingual interview support
- Integration with job portals and hiring platforms
- More accurate behavioral and emotion analysis models
