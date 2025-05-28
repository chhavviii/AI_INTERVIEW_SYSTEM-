from flask import render_template, request, jsonify

from app import app

# Option 1: Import individual services
from services.ocr_service import OCRService
from services.face_detection_service import FaceDetectionService
from services.speech_service import SpeechService
from services.llama_service import LlamaService

# Or Option 2: Import all services at once
# from app.services import OCRService, FaceDetectionService, SpeechService, LlamaService

import os
import numpy as np
import cv2

# Initialize services
ocr_service = OCRService()
face_detection = FaceDetectionService()
speech_service = SpeechService()
llama_service = LlamaService()

@app.route('/')
def index():
    return render_template('interview-system\templates\index.html')

@app.route('/candidate-form')
def candidate_form():
    return render_template('candidate_form.html')

@app.route('/interview-setup')
def interview_setup():
    return render_template('interview_setup.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        text = ocr_service.extract_text_from_pdf(file)
        if text:
            return jsonify({'text': text})
        return jsonify({'error': 'Could not extract text'}), 500

@app.route('/api/check-face', methods=['POST'])
def check_face():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    img_array = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    direction = face_detection.check_face_direction(frame)
    return jsonify({'direction': direction})

@app.route('/api/start-interview', methods=['POST'])
def start_interview():
    resume_text = request.json.get('resumeText')
    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400
    
    question = llama_service.generate_question(resume_text)
    if question:
        return jsonify({'question': question})
    return jsonify({'error': 'Could not generate question'}), 500

@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    data = request.json
    question = data.get('question')
    answer = data.get('answer')
    
    if not question or not answer:
        return jsonify({'error': 'Missing question or answer'}), 400
    
    evaluation = llama_service.evaluate_answer(question, answer)
    if evaluation:
        return jsonify({'evaluation': evaluation})
    return jsonify({'error': 'Could not evaluate answer'}), 500