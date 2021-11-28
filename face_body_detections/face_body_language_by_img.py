import pandas as pd
import pickle
with open('body_language.pkl','rb') as f:
    model = pickle.load(f)



import mediapipe as mp
import cv2
import numpy as np
import csv

mp_drawing = mp.solutions.drawing_utils #drawing helper
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)
face_imgs_names = ["happy.png","soso.png","yarn.png","away.png"]
face_imgs =[]

for i in range(4):
    face_imgs.append(cv2.imread("./../data/images/face_imgs/"+face_imgs_names[i]))

# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False        
        
        # Make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)
        
        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
        
        # Recolor image back to BGR for rendering
        image.flags.writeable = True   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 1. Draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                 )
        
        # 2. Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                 )

        # 3. Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                 )

        # 4. Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
        
        
        # Export coordinates
        #even if first img could not be taken landmarks, continue
        try:
            pose = results.pose_landmarks.landmark
            face = results.face_landmarks.landmark
            #extract pose landmarks, face landmarks to row by flatten method
            #flatten() is 2D or 3D array to 1D arrray
            #pose, face consist of  2D array
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            face_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in face]).flatten())

            #write before row to csv
            row = pose_row + face_row
            #insert class_name to rabel

    

            # with open('coords.csv', mode='a', newline='') as f:
            #     csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #     csv_writer.writerow(row) 
            x = pd.DataFrame([row])
            print(x)
            body_language_class = model.predict(x)[0]
            body_language_prob = model.predict_proba(x)[0]
            print(body_language_class, body_language_prob)

            cv2

        
        except:
            pass
        cv2.putText(image,"STATUS :"+str(body_language_class),(50,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

                        
        cv2.imshow('Raw Webcam Feed', image)

        if body_language_class == "Happy":
            print("happy")
            face_img = face_imgs[0]
        elif body_language_class =="Soso":
            face_img = face_imgs[1]
        elif body_language_class == "Yarn":
            face_img = face_imgs[2]
        elif body_language_class == "Away":
            face_img = face_imgs[3]

        cv2.imshow("Only Image" ,face_img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()