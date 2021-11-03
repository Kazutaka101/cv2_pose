import cv2 
import mediapipe as mp
import time
import inspect

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
h = 480
w = 800

#start and end ary X and y
numberAryStartH = int(h * 0.1)
numberAryStartW = int(w * 0.1)
numberAryH = int(h * 0.8)
numberAryW = int(w * 0.8)
print("start X, Y")
print(numberAryStartW,numberAryStartH)
print("end X , Y")
print(numberAryW, numberAryH)

sum = 0

#5 x 2 arry 
aryX = []
aryY = 0
print("--cal--")
aryXLen = numberAryW - numberAryStartW

xPerAry = int(aryXLen/5) 
print(xPerAry)
sum = 0

for k in range(4):
    sum = sum + xPerAry
    aryX.append(sum + numberAryStartW)

yLen = numberAryH - numberAryStartW
aryY = int(yLen / 2) + numberAryStartH

print("--aryX--")
print(aryX)
print("")
print("--aryY--")
print(aryY)

numberAryX = []
numberAryY = []

numberXlen = 0
#numberXLen = aryX[0] - numberAryStartW
#print(numberXLen)
#print(int(numberXLen/2) + numberAryStartW)

#numberX
for i in range(5):
    if i == 0:
        numberXlen = aryX[i] - numberAryStartW
        numberAryX.append(int(numberXlen/2) + numberAryStartW)
    elif i < 4:
        numberXlen = aryX[i] - aryX[i - 1]
        numberAryX.append(int(numberXlen/2) + aryX[i-1])
    else:
        numberXlen = numberAryW - aryX[3]
        numberAryX.append(int(numberXlen/2) + aryX[i-1])

#numberY
#yLen = numberAryH - numberAryStartW
numberAryY.append(int(aryY/2) + numberAryStartH)

yLen = numberAryH - aryY

numberAryY.append(int(yLen/2) + aryY)

print("---numberAryY---")
print(numberAryY)

print("---numberAryX---")
print(numberAryX)

while True:
    success, img = cap.read()
    img = cv2.resize(img,(w,h))
    img = cv2.flip(img, 1)
    #Pose Detection
    results = pose.process(img)

    if results.pose_landmarks:
       mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
    #outline
    #top
    cv2.line(img,(numberAryStartW,numberAryStartH),(numberAryW,numberAryStartH),(255,0,0),thickness=5)
    #left
    cv2.line(img,(numberAryStartW,numberAryStartH),(numberAryStartW,numberAryH),(255,0,0),thickness=5)
    #right
    cv2.line(img,(numberAryW,numberAryStartH),(numberAryW,numberAryH),(255,0.0),thickness=5)
    #bottom
    cv2.line(img,(numberAryStartW,numberAryH),(numberAryW,numberAryH),(255,0,0),thickness=5)

    #innerline vertical
    cv2.line(img,(aryX[0],numberAryStartH),(aryX[0],numberAryH),(255,0,0),thickness=5)
    cv2.line(img,(aryX[1],numberAryStartH),(aryX[1],numberAryH),(255,0,0),thickness=5)
    cv2.line(img,(aryX[2],numberAryStartH),(aryX[2],numberAryH),(255,0,0),thickness=5)
    cv2.line(img,(aryX[3],numberAryStartH),(aryX[3],numberAryH),(255,0,0),thickness=5)
    
    #innerline holizoncal
    cv2.line(img,(numberAryStartW,aryY),(numberAryW,aryY),(255,0,0),thickness=5)

    #draw number
    
    cv2.putText(img, "0", (numberAryX[0], numberAryY[0]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)
    cv2.putText(img, "1", (numberAryX[1], numberAryY[0]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)
    cv2.putText(img, "2", (numberAryX[2], numberAryY[0]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)
    cv2.putText(img, "3", (numberAryX[3], numberAryY[0]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)
    cv2.putText(img, "4", (numberAryX[4], numberAryY[0]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)
    
    cv2.putText(img, "5", (numberAryX[0], numberAryY[1]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)
    cv2.putText(img, "6", (numberAryX[1], numberAryY[1]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)
    cv2.putText(img, "7", (numberAryX[2], numberAryY[1]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)
    cv2.putText(img, "8", (numberAryX[3], numberAryY[1]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)
    cv2.putText(img, "9", (numberAryX[4], numberAryY[1]),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255,0 ), 3, cv2.LINE_AA)

    





    
    
    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("sample", img)




