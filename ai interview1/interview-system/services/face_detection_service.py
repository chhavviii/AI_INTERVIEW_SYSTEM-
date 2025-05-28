import cv2
import mediapipe as mp

class FaceDetectionService:
    def __init__(self):
        pass

    def check_face_direction(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image)
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            
            # Get nose landmark
            nose = face_landmarks.landmark[4]
            
            # Calculate face direction based on nose position
            image_height, image_width = image.shape[:2]
            nose_x = int(nose.x * image_width)
            center_x = image_width // 2
            
            threshold = image_width * 0.1
            
            if abs(nose_x - center_x) < threshold:
                return "front"
            elif nose_x < center_x - threshold:
                return "left"
            else:
                return "right"
                
        return None

    def __del__(self):
        self.face_mesh.close()