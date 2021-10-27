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

mpDraw = mp.solutions.drawing_utils
#モデルの選択
mpPose = mp.solutions.pose
#Poseモデルの作成
pose = mpPose.Pose(static_image_mode=False,
                model_complexity=0,
                smooth_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)
h=400
w=400
cap = cv2.VideoCapture(-1)
pTime=0
success, img = cap.read()
imgH = 200 
imgW = 200  
imgMidH = int(imgH/2)
imgMidW = int(imgW/2)
smile = cv2.imread("smile.jpg",-1)
smile = cv2.resize(smile,(imgH,imgW))
while True:
    success, img = cap.read()
    #BGR => RGB変換
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #RGB画像に対して解析をかける。
    results = pose.process(imgRGB)
    #resultsにlandmarkがあれば解析できている
    resized_img = cv2.resize(img,(h,w))
    try:
        landmarks = results.pose_landmarks.landmark
        #骨格を描画、線を引く POSE_CONNECTIONSを消せば骨格点だけ
        mpDraw.draw_landmarks(resized_img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        #print(landmarks[mpPose.PoseLandmark.NOSE.value])
        noseX = (int(landmarks[mpPose.PoseLandmark.NOSE.value].x*w))
        noseY = (int(landmarks[mpPose.PoseLandmark.NOSE.value].y*h))
        print("noseX:" + str(noseX))
        print("noseY:" + str(noseY))
        print("")
        resized_img[(noseY-imgMidW):(noseY+imgMidW),(noseX-imgMidH):(noseX+imgMidH)] = smile[0:imgW,0:imgH]
        print("noseX1 = " + str(noseX-imgMidW))
        print("noseY1 = " + str(noseY-imgMidH))
        print("")
    except:
        #landmarkがなければエラーが出てしまう。
        pass

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    #draw FPS
    cv2.putText(resized_img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)
    cv2.imshow("Image",resized_img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.relase()
cv2.destroyAllWindows()
