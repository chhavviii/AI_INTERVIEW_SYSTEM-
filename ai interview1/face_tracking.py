import cv2
import mediapipe as mp
import numpy as np

def main():
    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # Start video capture
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            
            # Get nose direction (landmark 1 is nose tip)
            nose = face_landmarks.landmark[1]
            h, w, _ = frame.shape
            nose_x = int(nose.x * w)
            nose_y = int(nose.y * h)
            nose_z = nose.z
            
            # Calculate head rotation based on nose direction
            # These thresholds might need adjustment
            looking_away = False
            
            # Check x-axis rotation (left-right)
            if abs(nose.x - 0.5) > 0.1:
                looking_away = True
                
            # Check y-axis rotation (up-down)
            if abs(nose.y - 0.5) > 0.1:
                looking_away = True
                
            # Check z-axis (depth)
            if abs(nose_z) > 0.1:
                looking_away = True
            
            # Draw face mesh
            face_points = np.array([(int(landmark.x * w), int(landmark.y * h)) 
                                  for landmark in face_landmarks.landmark])
            
            if looking_away:
                # Draw red connections and warning
                cv2.polylines(frame, [face_points], True, (0, 0, 255), 1)
                cv2.putText(frame, "Please look forward!", 
                          (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                          1, (0, 0, 255), 2)
            else:
                # Draw green connections
                cv2.polylines(frame, [face_points], True, (0, 255, 0), 1)
        
        # Display the frame
        cv2.imshow("Face Tracking", frame)
        
        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()