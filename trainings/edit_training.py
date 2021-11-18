import cv2
import time
import mediapipe as mp
import numpy as np
import time
import argparse

parser = argparse.ArgumentParser(description="cnt and report ur training")
parser.add_argument('--cnt', type=int,default=10)
parser.add_argument('--mode',type=str,default="squat",help="squat/ push-up / arm curl")
args = parser.parse_args()
print(args)

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture("/home/kazutaka/codes/mediapipe_pose/data/videos/training_videos/squat.mp4")
pTime=0


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

def getModeNum(mode,modes):
    ans = "None"
    for i in range(len(modes)):
        if mode == modes[i]:
            ans = mode
            break
    return mode

cntForMode = 0
trainingModeNum = 0
modes = ["ARMCURL", "SQUAT", "PUSH-UP"]
for i in range(3):
    if modes[i] == args.mode:
        trainingModeNum = i
        mode = modes[i]
mode = modes[trainingModeNum]   
cnt = 0
isBent = False



    
selectedModeNum = 2
startTime = time.time()
limitCnt = args.cnt

while True:
   
    if selectedModeNum == 2:
        success, img = cap.read()
        img = cv2.resize(img, (640,480))
        #descript key
        

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        #Detect here
        results = pose.process(imgRGB)

        #If detected pose estimation
        #POSE_CONNECTION = point to point line
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        

        #wait 3 sec at execed

        #extract specific landmark
        try:
            #----example extract specific landmark----
            #landmarks[mpPose.PoseLandmark.NOSE.value]

            #all landmark
            landmarks = results.pose_landmarks.landmark

            #detect down and up, mode switch
            if trainingModeNum == 0:
                Rshoulder = [landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].y]
                Relbow = [landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].y]
                Rwrist =[landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].y]
                angle = cal_angle(Rshoulder, Relbow, Rwrist)
                if angle >= 160:
                    if isBent is True:
                        isBent = False

                elif angle <= 90:
                    if isBent is False:
                        #playsound("./pingpong.mp3")
                        cnt = cnt + 1 
                        isBent = True

                    elif isBent is True:
                        pass
                cv2.putText(img, str(angle), tuple(np.multiply(Relbow, [640,480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

            elif trainingModeNum == 1:
                Rhip = [landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].y]
                Rknee = [landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].y]
                Rankle = [landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].y]
                Lanke = [landmarks[mpPose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mpPose.PoseLandmark.LEFT_ANKLE.value].y]
                Rfoot = [landmarks[mpPose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mpPose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
                Lfoot = [landmarks[mpPose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mpPose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                angle = cal_angle(Rhip,Rknee,Rankle)
                if angle >= 160:
                    if isBent is True:
                        isBent = False
                        #cheking form by  Rfoot.x - Rankle.x
                        rightDiff = Rfoot[0] - Rankle[0]
                        print("---right---")
                        print(rightDiff) 

                        #cheking form by Lanke.x - Lfoot.x
                        leftDiff = Lanke[0] - Lfoot[0]
                        print("---left---")
                        print(leftDiff)
                elif angle <= 90:
                    if isBent is False:
                        cnt = cnt + 1 
                        isBent = True

                    elif isBent is True:
                        pass
                
                cv2.putText(img, str(angle), tuple(np.multiply(Rknee, [640,480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            
            elif trainingModeNum == 2:
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



            #show angle
                                    
        except:
            pass

        #show cnt
        cv2.putText(img,"COUNT :+"+str(cnt),(50,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

        #show up or down
        if isBent is False:
            cv2.putText(img,"STATUS :NOT BENTING",(50,100),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

        else:
            cv2.putText(img,"STATUS :BENTING",(50,100),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)        

        key = cv2.waitKey(1) & 0xFF

        #show mode
        cv2.putText(img,"MODE :" + str(mode),(330,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)


        
        cv2.imshow("Image",img)


        cv2.waitKey(1)

cap.relase()
cv2.destroyAllWindows()
