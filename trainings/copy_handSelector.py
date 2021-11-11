import cv2 
import mediapipe as mp
import time
import inspect

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

pose = mpPose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
h = 900
w = 1600


#start and end ary X and y
numberAryStartH = int(h * 0.1)
numberAryStartW = int(w * 0.1)
numberAryH = int(h * 0.8)
numberAryW = int(w * 0.8)
print("start X, Y")
print(numberAryStartW,numberAryStartH)
print("end X , Y")
print(numberAryW, numberAryH)

okButtonX = int(w * 0.85)
okButtonY = int(h * 0.85)
print("ok button X, Y")
print(okButtonX, okButtonY)


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
showNums = ""
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

#selected number X, Y
fromSelectedNumX = int(w*0.85)
fromSelectedNumY = int(h*0.1) 

print("--fromSelectedNumX and Y")
print(fromSelectedNumX,fromSelectedNumY)

selectedNumX = int((w - fromSelectedNumX)/2) + fromSelectedNumX
selectedNumY = int(fromSelectedNumY / 2)

print("--selectedNumX---")
print(selectedNumX, selectedNumY)

selectedNum = "None"
#1000... => 0
#0100...=> 1
NumberBin = 0b0000000000
stime = time.time()
passTime = 0
selectedNums = []
modiY = numberAryH * 0.1

while True:
    success, img = cap.read()
    img = cv2.resize(img,(w,h))
    img = cv2.flip(img, 1)
    #Pose Detection
    results = pose.process(img)
    
    #drawing line between  connection to connection  
    #if results.pose_landmarks:
    #   mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)


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

    #delete button

    #ok button
    cv2.line(img,(okButtonX, okButtonY ),(w,okButtonY),(255,0,0),thickness=5)
    cv2.line(img,(okButtonX, okButtonY ),(okButtonX,h),(255,0,0),thickness=5)
    cv2.line(img,(okButtonX, h),(w,h),(255,0,0),thickness=5)
    cv2.line(img,(w, okButtonY ),(w,h),(255,0,0),thickness=5)
    





    #detect hand on NumberArray
    
    try:
        landmarks = results.pose_landmarks.landmark
        rightWRIST = [landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].y]
        leftWRIST = [landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].y]
        x = rightWRIST[0]*w 
        y = rightWRIST[1]*h

        x1 = leftWRIST[0] * w
        y1 = leftWRIST[1] * h
        
        #数字ではなく、高さの割合で出すべき
        y = y - modiY
        y1 = y1 - modiY

        cv2.circle(img, (int(x),int(y)), 50, (0,0,255), thickness=-1, lineType=cv2.LINE_8, shift=0)
        cv2.circle(img, (int(x1),int(y1)), 50, (0,0,255), thickness=-1, lineType=cv2.LINE_8, shift=0)
        
        
        #print(x, y)

        #detect hand on top NumberArray
        if (numberAryStartW < x and numberAryStartH < y and aryX[0] > x and aryY > y) or (numberAryStartW < x1 and numberAryStartH < y1 and aryX[0] > x1 and aryY > y1):
            selectedNum = "0"
            #0が立っていない、つまり、初期状態である
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b1000000000

            #この対応indexに1が立っている。つまり、前と同じ場所にとどまっている。
            elif NumberBin == 0b1000000000:
                #proceed timer
                #この対応index以外に1が立っている。つまり、違う場所から来たのである。

                etime = time.time()
 
            else:
                #タイマーをリセットして、このindexを代入する
                #timer reset
                stime = time.time()
                NumberBin = 0b1000000000
            
        
        elif (aryX[0] < x and numberAryStartH < y and aryX[1] > x and aryY > y) or (aryX[0] < x1 and numberAryStartH < y1 and aryX[1] > x1 and aryY > y1):
            selectedNum = "1"
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b0100000000

            elif NumberBin == 0b0100000000:
                etime = time.time()
    
            else:
                stime = time.time()
                NumberBin = 0b0100000000
            
        elif (aryX[1] < x and numberAryStartH < y and aryX[2] > x and aryY > y) or (aryX[1] < x1 and numberAryStartH < y1 and aryX[2] > x1 and aryY > y1):
            selectedNum = "2"
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b0010000000

            elif NumberBin == 0b0010000000:
                etime = time.time()
     
            else:
                stime = time.time()
                NumberBin = 0b0010000000

        elif (aryX[2] < x and numberAryStartH < y and aryX[3] > x and aryY > y) or (aryX[2] < x1 and numberAryStartH < y1 and aryX[3] > x1 and aryY > y1) :
            selectedNum = "3"
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b0001000000

            elif NumberBin == 0b0001000000:
                etime = time.time()
   
            else:
                stime = time.time()
                NumberBin = 0b0001000000

        elif (aryX[3] < x and numberAryStartH < y and numberAryW > x and aryY > y) or (aryX[3] < x1 and numberAryStartH < y1 and numberAryW > x1 and aryY > y1):
            selectedNum = "4"
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b0000100000

            elif NumberBin == 0b0000100000:
                etime = time.time()
   
            else:
                stime = time.time()
                NumberBin = 0b0000100000

        #detect hand on bottom NumberArray
        elif (numberAryStartW < x and aryY < y and aryX[0] > x and numberAryH > y) or (numberAryStartW < x1 and aryY < y1 and aryX[0] > x1 and numberAryH > y1):
            selectedNum = "5"
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b0000010000

            elif NumberBin == 0b0000010000:
                etime = time.time()
     
            else:
                stime = time.time()
                NumberBin = 0b0000010000
        elif (aryX[0] < x and aryY < y and aryX[1] > x and numberAryH > y) or (aryX[0] < x1 and aryY < y1 and aryX[1] > x1 and numberAryH > y1):
            selectedNum = "6"
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b0000001000

            elif NumberBin == 0b0000001000:
                etime = time.time()
  
            else:
                stime = time.time()
                NumberBin = 0b0000001000
        elif (aryX[1] < x and aryY < y and aryX[2] > x and numberAryH > y) or (aryX[1] < x1 and aryY < y1 and aryX[2] > x1 and numberAryH > y1):
            selectedNum = "7"
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b0000000100

            elif NumberBin == 0b0000000100:
                etime = time.time()

            else:
                stime = time.time()
                NumberBin = 0b0000000100
        elif (aryX[2] < x and aryY < y and aryX[3] > x and numberAryH > y) or (aryX[2] < x1 and aryY < y1 and aryX[3] > x1 and numberAryH > y1) :            
            selectedNum = "8"
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b0000000010

            elif NumberBin == 0b0000000010:
                etime = time.time()
  
            else:
                stime = time.time()
                NumberBin = 0b0000000010
        elif (aryX[3] < x and aryY < y and numberAryW > x and numberAryH > y) or (aryX[3] < x1 and aryY < y1 and numberAryW > x1 and numberAryH > y1): 
            selectedNum = "9"
            if NumberBin & 0b1111111111 == 0:
                NumberBin = 0b0000000001

            elif NumberBin == 0b0000000001:
                etime = time.time()
                
            else:
                stime = time.time()
                NumberBin = 0b0000000001
        #ok Button detection
        elif x > okButtonX and y > okButtonY and x < w and y < h:
            print("aaa")
        else:
            selectedNum = "None"
            stime = time.time()



        passTime = etime - stime
        #print(passTime)


    except:
        #print("Error Occuerd")
        #import traceback
        #traceback.print_exc()
        pass
    #draw selected number. it should be counter  3 2 1
    if passTime < 0:
        cv2.putText(img,"2", (selectedNumX,selectedNumY),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
    else:
        timer =  2 - int(passTime)
        #3秒たった
        if timer < 0:
            selectedNums.append(selectedNum)
            stime = time.time()

        cv2.putText(img,str(timer), (selectedNumX,selectedNumY),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)

    #draw selected numbers
    showNumX = int(w * 0.1)
    showNumY = int(h * 0.9)
    showNums = "".join(selectedNums)
    cv2.putText(img,showNums, (showNumX,showNumY),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA)
    #print(selectedNums)


    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("sample", img)




