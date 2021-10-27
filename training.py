# 0: PoseLandmark.NOSE
# 1: PoseLandmark.LEFT_EYE_INNER
# 2: PoseLandmark.LEFT_EYE
# 3: PoseLandmark.LEFT_EYE_OUTER
# 4: PoseLandmark.RIGHT_EYE_INNER
# 5: PoseLandmark.RIGHT_EYE
# 6: PoseLandmark.RIGHT_EYE_OUTER
# 7: PoseLandmark.LEFT_EAR
# 8: PoseLandmark.RIGHT_EAR
# 9: PoseLandmark.MOUTH_LEFT
# 10: PoseLandmark.MOUTH_RIGHT
# 11: PoseLandmark.LEFT_SHOULDER
# 12: PoseLandmark.RIGHT_SHOULDER
# 13: PoseLandmark.LEFT_ELBOW
# 14: PoseLandmark.RIGHT_ELBOW
# 15: PoseLandmark.LEFT_WRIST
# 16: PoseLandmark.RIGHT_WRIST
# 17: PoseLandmark.LEFT_PINKY
# 18: PoseLandmark.RIGHT_PINKY
# 19: PoseLandmark.LEFT_INDEX
# 20: PoseLandmark.RIGHT_INDEX
# 21: PoseLandmark.LEFT_THUMB
# 22: PoseLandmark.RIGHT_THUMB
# 23: PoseLandmark.LEFT_HIP
# 24: PoseLandmark.RIGHT_HIP
# 25: PoseLandmark.LEFT_KNEE
# 26: PoseLandmark.RIGHT_KNEE
# 27: PoseLandmark.LEFT_ANKLE
# 28: PoseLandmark.RIGHT_ANKLE
# 29: PoseLandmark.LEFT_HEEL
# 30: PoseLandmark.RIGHT_HEEL
# 31: PoseLandmark.LEFT_FOOT_INDEX
# 32: PoseLandmark.RIGHT_FOOT_INDEX


import cv2
import time
import mediapipe as mp
import numpy as np
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
pTime=0
success, img = cap.read()

#a = shoulder
#b = elbow
#c = sholder
def cal_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

cntForMode = 0
modeIdx = 0
modes = ["ARM CURL", "SQUAT", "PUSH-UPS" ]
mode = modes[modeIdx]



def changeMode(a):
    global modeIdx
    global modes
    modeIdx = int(a%3)
    mode = modes[modeIdx]
    print(modeIdx)
    print(mode)
    return mode

cnt = 0
isBent = False

while True:
    success, img = cap.read()
    #descript key
    cv2.putText(img,"'s' to start",(0,450),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),1)
    cv2.putText(img,"'p' to pose",(0,470),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),1)
    cv2.putText(img,"'r' to reset count",(150,450),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),1)
    cv2.putText(img,"'q' to quit",(150,470),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),1)




    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    #Detect here
    results = pose.process(imgRGB)

    #If detected pose estimation
    #POSE_CONNECTION = point to point line
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
    
    #extract specific landmark
    try:
        #----example extract specific landmark----
        #landmarks[mpPose.PoseLandmark.NOSE.value]

        #all landmark
        landmarks = results.pose_landmarks.landmark

        #detect down and up, mode switch
        if modeIdx == 0:
            Rshoulder = [landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].y]
            Relbow = [landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].y]
            Rwrist =[landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].y]
            angle = cal_angle(Rshoulder, Relbow, Rwrist)
            if angle >= 160:
                if isBent is True:
                    isBent = False

            elif angle <= 90:
                if isBent is False:
                    cnt = cnt + 1 
                    isBent = True

                elif isBent is True:
                    pass
            cv2.putText(img, str(angle), tuple(np.multiply(Relbow, [640,480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        elif modeIdx == 1:
            Rhip = [landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].y]
            Rknee = [landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].y]
            Rankle = [landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].y]
            angle = cal_angle(Rhip,Rknee,Rankle)
            print(angle)
            if angle >= 160:
                if isBent is True:
                    isBent = False

            elif angle <= 90:
                if isBent is False:
                    cnt = cnt + 1 
                    isBent = True

                elif isBent is True:
                    pass
            
            cv2.putText(img, str(angle), tuple(np.multiply(Rknee, [640,480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        
        elif modeIdx == 2:
            print("")
 


        #show angle
        
                                

                    
    except:
        pass

    #show cnt
    cv2.putText(img,"COUNT :+"+str(cnt),(50,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

    #show up or down
    if isBent is False:
        cv2.putText(img,"STATUS :DOWN",(50,100),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
    else:
        cv2.putText(img,"STATUS :UP",(50,100),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

    key = cv2.waitKey(1) & 0xFF

    #show mode
    cv2.putText(img,"MODE :" + str(mode),(330,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

    
    #get key
    if key == ord('q'):
        break

    #reset cnt
    if key == ord('r'):
        cnt = 0
    
    #start counting
    if key == ord('s'):
        print("start")

    #pose counting
    if key == ord('p'):
        print("stop")

    if key == ord('m'):
        print("changemode")
        cntForMode = cntForMode + 1
        mode = changeMode(cntForMode)

    
    #resized_img = cv2.resize(img,(800,400))
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)

cap.relase()
cv2.destroyAllWindows()