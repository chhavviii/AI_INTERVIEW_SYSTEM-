from setuptools import setup, find_packages

setup(
    name="interview-system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'opencv-python',
        'pytesseract',
        'python-dotenv',
        'SpeechRecognition',
        'pyttsx3',
        'mediapipe',
        'PyPDF2',
        'numpy'
    ],
)