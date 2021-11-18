import cv2
import mediapipe as mp
import time
import inspect
import numpy as np

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

pose = mpPose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# 000000
cap = cv2.VideoCapture(0)
h = 900
w = 1600


# start and end ary X and y
numberAryStartH = int(h * 0.1)
numberAryStartW = int(w * 0.1)
numberAryH = int(h * 0.8)
numberAryW = int(w * 0.8)
print("start X, Y")
print(numberAryStartW, numberAryStartH)
print("end X , Y")
print(numberAryW, numberAryH)


sum = 0

# 5 x 2 arry
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

okButtonStartX = int(w * 0.85)
okButtonStartY = numberAryStartH
print("ok button X, Y")
print(okButtonStartX, okButtonStartY)

okButtonEndX = w
okButtonEndY = aryY

okButtonMidX = int((okButtonEndX - okButtonStartX) / 2) + okButtonStartX
okButtonMidY = int((okButtonEndY - okButtonStartY) / 2) + okButtonStartY


# delete Button
deleteButtonStartX = okButtonStartX
deleteButtonStartY = okButtonEndY
deleteButtonEndX = w
deleteButtonEndY = numberAryH

deleteButtonMidX = int(
    (deleteButtonEndX - deleteButtonStartX) / 2) + deleteButtonStartX
deleteButtonMidY = int(
    (deleteButtonEndY - deleteButtonStartY) / 2) + deleteButtonStartY

modeArrayStartX = int(w * 0.1)
modeArrayStartY = int(h * 0.1)
modeArrayEndX = int(w * 0.8)
modeArrayEndY = int(h * 0.8)

modeArrayLen = modeArrayEndX - modeArrayStartX
modeArrayPerCel = int(modeArrayLen / 3)
modeArraysX = []
sum = 0
for i in range(2):
    sum += modeArrayPerCel
    modeArraysX.append(sum + modeArrayStartX)
print(modeArraysX)

modeArraysMidX = []
modeArrayMidLen = 0
modeArraysMidX.append(modeArrayStartX + int(w*0.05))
modeArraysMidX.append(modeArraysX[0] + int(w * 0.05))
modeArraysMidX.append(modeArraysX[1] + int(w * 0.05))

modeArraysMidY = int((modeArrayEndY - modeArrayStartY)/2) + modeArrayStartY


numberAryX = []
numberAryY = []

numberXlen = 0
showNums = ""
showTextX = int(w * 0.1)
showTextY = int(h * 0.9)
ok = False
selectedMode = ""

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

# numberY
#yLen = numberAryH - numberAryStartW
numberAryY.append(int(aryY/2) + numberAryStartH)

yLen = numberAryH - aryY

numberAryY.append(int(yLen/2) + aryY)

print("---numberAryY---")
print(numberAryY)

print("---numberAryX---")
print(numberAryX)

# selected number X, Y
fromSelectedNumX = int(w*0.85)
fromSelectedNumY = int(h*0.1)

print("--fromSelectedNumX and Y")
print(fromSelectedNumX, fromSelectedNumY)

selectedNumX = int((w - fromSelectedNumX)/2) + fromSelectedNumX
selectedNumY = int(fromSelectedNumY / 2)

print("--selectedNumX---")
print(selectedNumX, selectedNumY)

selectedNum = "None"
# 1000... => 0
# 0100...=> 1
NumberBin = 0b000000000000
ModeBin = 0b000
stime = time.time()
passTime = 0
selectedNums = []
modiY = numberAryH * 0.1

# SWITCHED MODE 0 TO 1 for debugging !!
selectModeNum = 0
showSelectedMode = ""


def cal_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle


modes = ["ARMCURL", "SQUAT", "PUSH-UP"]


def getModeNum(mode, modes):
    ans = "None"
    for i in range(len(modes)):
        if mode == modes[i]:
            ans = i
            break
    return ans


cnt = 0
isBent = False

limitCnt = 0


while True:
    success, img = cap.read()
    img = cv2.resize(img, (w, h))
    img = cv2.flip(img, 1)
    # Pose Detection
    results = pose.process(img)

    # drawing line between  connection to connection
    # if results.pose_landmarks:
    #   mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)

    # outline
    # top

    if selectModeNum == 1:
        cv2.line(img, (numberAryStartW, numberAryStartH),
                 (numberAryW, numberAryStartH), (255, 0, 0), thickness=5)
        # left
        cv2.line(img, (numberAryStartW, numberAryStartH),
                 (numberAryStartW, numberAryH), (255, 0, 0), thickness=5)
        # right
        cv2.line(img, (numberAryW, numberAryStartH),
                 (numberAryW, numberAryH), (255, 0.0), thickness=5)
        # bottom
        cv2.line(img, (numberAryStartW, numberAryH),
                 (numberAryW, numberAryH), (255, 0, 0), thickness=5)

        # innerline vertical
        cv2.line(img, (aryX[0], numberAryStartH),
                 (aryX[0], numberAryH), (255, 0, 0), thickness=5)
        cv2.line(img, (aryX[1], numberAryStartH),
                 (aryX[1], numberAryH), (255, 0, 0), thickness=5)
        cv2.line(img, (aryX[2], numberAryStartH),
                 (aryX[2], numberAryH), (255, 0, 0), thickness=5)
        cv2.line(img, (aryX[3], numberAryStartH),
                 (aryX[3], numberAryH), (255, 0, 0), thickness=5)

        # innerline holizoncal
        cv2.line(img, (numberAryStartW, aryY),
                 (numberAryW, aryY), (255, 0, 0), thickness=5)

        # draw number

        cv2.putText(img, "0", (numberAryX[0], numberAryY[0]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "1", (numberAryX[1], numberAryY[0]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "2", (numberAryX[2], numberAryY[0]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "3", (numberAryX[3], numberAryY[0]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "4", (numberAryX[4], numberAryY[0]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)

        cv2.putText(img, "5", (numberAryX[0], numberAryY[1]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "6", (numberAryX[1], numberAryY[1]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "7", (numberAryX[2], numberAryY[1]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "8", (numberAryX[3], numberAryY[1]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "9", (numberAryX[4], numberAryY[1]),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)

        # delete button
        cv2.line(img, (deleteButtonEndX, deleteButtonStartY),
                 (deleteButtonEndX, deleteButtonEndY), (255, 0, 0), thickness=5)
        cv2.line(img, (deleteButtonStartX, deleteButtonEndY),
                 (deleteButtonEndX, deleteButtonEndY), (255, 0, 0), thickness=5)
        cv2.line(img, (deleteButtonStartX, deleteButtonStartY),
                 (deleteButtonStartX, deleteButtonEndY), (255, 0, 0), thickness=5)

        cv2.putText(img, "DEL", (deleteButtonMidX, deleteButtonMidY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)

    elif selectModeNum == 0:
        # draw mode select array
        cv2.line(img, (modeArrayStartX, modeArrayStartY),
                 (modeArrayStartX, modeArrayEndY), (255, 0, 0), thickness=5)
        cv2.line(img, (modeArrayStartX, modeArrayStartY),
                 (modeArrayEndX, modeArrayStartY), (255, 0, 0), thickness=5)
        cv2.line(img, (modeArrayStartX, modeArrayEndY),
                 (modeArrayEndX, modeArrayEndY), (255, 0, 0), thickness=5)
        cv2.line(img, (modeArrayEndX, modeArrayStartY),
                 (modeArrayEndX, modeArrayEndY), (255, 0, 0), thickness=5)

        cv2.line(img, (modeArraysX[0], modeArrayStartY),
                 (modeArraysX[0], modeArrayEndY), (255, 0, 0), thickness=5)
        cv2.line(img, (modeArraysX[1], modeArrayStartY),
                 (modeArraysX[1], modeArrayEndY), (255, 0, 0), thickness=5)
        cv2.putText(img, "ARM CURL", (modeArraysMidX[0], modeArraysMidY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "SQUAT", (modeArraysMidX[1], modeArraysMidY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.putText(img, "PUSH-UP", (modeArraysMidX[2], modeArraysMidY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)

    # ok button
    if selectModeNum != 2:
        cv2.line(img, (okButtonStartX, okButtonStartY),
                 (okButtonEndX, okButtonStartY), (255, 0, 0), thickness=5)
        cv2.line(img, (okButtonStartX, okButtonStartY),
                 (okButtonStartX, okButtonEndY), (255, 0, 0), thickness=5)
        cv2.line(img, (okButtonStartX, okButtonEndY),
                 (okButtonEndX, okButtonEndY), (255, 0, 0), thickness=5)
        cv2.line(img, (okButtonEndX, okButtonStartY),
                 (okButtonEndX, okButtonEndY), (255, 0, 0), thickness=5)
        cv2.putText(img, "Ok", (okButtonMidX, okButtonMidY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)

    # detect hand on NumberArray

    try:
        if selectModeNum != 2:
            landmarks = results.pose_landmarks.landmark
            rightWRIST = [landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].x,
                          landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].y]
            leftWRIST = [landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].y]
            x = rightWRIST[0]*w
            y = rightWRIST[1]*h

            x1 = leftWRIST[0] * w
            y1 = leftWRIST[1] * h

            # 数字ではなく、高さの割合で出すべき
            y = y - modiY
            y1 = y1 - modiY

            cv2.circle(img, (int(x), int(y)), 50, (0, 0, 255),
                       thickness=-1, lineType=cv2.LINE_8, shift=0)
            cv2.circle(img, (int(x1), int(y1)), 50, (0, 0, 255),
                       thickness=-1, lineType=cv2.LINE_8, shift=0)

        #print(x, y)

        # detect hand on top NumberArray
        if selectModeNum == 1:
            if (numberAryStartW < x and numberAryStartH < y and aryX[0] > x and aryY > y) or (numberAryStartW < x1 and numberAryStartH < y1 and aryX[0] > x1 and aryY > y1):
                selectedNum = "0"
                # 0が立っていない、つまり、初期状態である
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b100000000000

                # この対応indexに1が立っている。つまり、前と同じ場所にとどまっている。
                elif NumberBin == 0b100000000000:
                    # proceed timer
                    # この対応index以外に1が立っている。つまり、違う場所から来たのである。

                    etime = time.time()

                else:
                    # タイマーをリセットして、このindexを代入する
                    # timer reset
                    stime = time.time()
                    NumberBin = 0b100000000000

            elif (aryX[0] < x and numberAryStartH < y and aryX[1] > x and aryY > y) or (aryX[0] < x1 and numberAryStartH < y1 and aryX[1] > x1 and aryY > y1):
                selectedNum = "1"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b010000000000

                elif NumberBin == 0b010000000000:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b010000000000

            elif (aryX[1] < x and numberAryStartH < y and aryX[2] > x and aryY > y) or (aryX[1] < x1 and numberAryStartH < y1 and aryX[2] > x1 and aryY > y1):
                selectedNum = "2"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b001000000000

                elif NumberBin == 0b001000000000:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b001000000000

            elif (aryX[2] < x and numberAryStartH < y and aryX[3] > x and aryY > y) or (aryX[2] < x1 and numberAryStartH < y1 and aryX[3] > x1 and aryY > y1):
                selectedNum = "3"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b000100000000

                elif NumberBin == 0b000100000000:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b000100000000

            elif (aryX[3] < x and numberAryStartH < y and numberAryW > x and aryY > y) or (aryX[3] < x1 and numberAryStartH < y1 and numberAryW > x1 and aryY > y1):
                selectedNum = "4"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b000010000000

                elif NumberBin == 0b000010000000:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b000010000000

            # detect hand on bottom NumberArray
            elif (numberAryStartW < x and aryY < y and aryX[0] > x and numberAryH > y) or (numberAryStartW < x1 and aryY < y1 and aryX[0] > x1 and numberAryH > y1):
                selectedNum = "5"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b000001000000

                elif NumberBin == 0b000001000000:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b000001000000
            elif (aryX[0] < x and aryY < y and aryX[1] > x and numberAryH > y) or (aryX[0] < x1 and aryY < y1 and aryX[1] > x1 and numberAryH > y1):
                selectedNum = "6"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b000000100000

                elif NumberBin == 0b000000100000:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b000000100000
            elif (aryX[1] < x and aryY < y and aryX[2] > x and numberAryH > y) or (aryX[1] < x1 and aryY < y1 and aryX[2] > x1 and numberAryH > y1):
                selectedNum = "7"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b000000010000

                elif NumberBin == 0b000000010000:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b000000010000
            elif (aryX[2] < x and aryY < y and aryX[3] > x and numberAryH > y) or (aryX[2] < x1 and aryY < y1 and aryX[3] > x1 and numberAryH > y1):
                selectedNum = "8"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b000000001000

                elif NumberBin == 0b000000001000:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b000000001000
            elif (aryX[3] < x and aryY < y and numberAryW > x and numberAryH > y) or (aryX[3] < x1 and aryY < y1 and numberAryW > x1 and numberAryH > y1):
                selectedNum = "9"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b000000000100

                elif NumberBin == 0b000000000100:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b000000000100
            # ok Button detection
            elif x1 > okButtonStartX and y1 > okButtonStartY and x1 < okButtonEndX and y1 < okButtonEndY:
                selectedNum = "OK"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b00000000010

                elif NumberBin == 0b00000000010:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b000000000010

            # delete Button detection
            elif x1 > deleteButtonStartX and y1 > deleteButtonStartY and x1 < deleteButtonEndX and y1 < deleteButtonEndY:
                selectedNum = "DEL"
                if NumberBin & 0b111111111111 == 0:
                    NumberBin = 0b00000000001

                elif NumberBin == 0b00000000001:
                    etime = time.time()

                else:
                    stime = time.time()
                    NumberBin = 0b000000000001

            else:
                selectedNum = "None"
                stime = time.time()

            passTime = etime - stime
            # print(passTime)

        elif selectModeNum == 0:
            # check hit ARMCURL BOX
            if (modeArrayStartX < x and modeArrayStartY < y and modeArraysX[0] > x and modeArrayEndY > y) or (modeArrayStartX < x1 and modeArrayStartY < y1 and modeArraysX[0] > x1 and modeArrayEndY > y1):
                selectedMode = "ARMCURL"
                # 0が立っていない、つまり、初期状態である
                if ModeBin & 0b1111 == 0:
                    ModeBin = 0b1000

                # この対応indexに1が立っている。つまり、前と同じ場所にとどまっている。
                elif ModeBin == 0b1000:
                    etime = time.time()

                else:
                    # タイマーをリセットして、このindexを代入する
                    # timer reset
                    stime = time.time()
                    ModeBin = 0b1000
            # check hit SQUAT BOX
            elif (modeArraysX[0] < x and modeArrayStartY < y and modeArraysX[1] > x and modeArrayEndY > y) or (modeArraysX[0] < x1 and modeArrayStartY < y1 and modeArraysX[1] > x1 and modeArrayEndY > y1):
                selectedMode = "SQUAT"
                if ModeBin & 0b1111 == 0:
                    ModeBin = 0b0100
                elif ModeBin == 0b0100:
                    etime = time.time()
                else:
                    stime = time.time()
                    ModeBin = 0b0100
            # chek hit PUSH-UP
            elif (modeArraysX[1] < x and modeArrayStartY < y and modeArrayEndX > x and modeArrayEndY > y) or (modeArraysX[1] < x1 and modeArrayStartY < y1 and modeArrayEndX > x1 and modeArrayEndY > y1):
                selectedMode = "PUSH-UP"
                if ModeBin & 0b1111 == 0:
                    ModeBin = 0b0010
                elif ModeBin == 0b0010:
                    etime = time.time()
                else:
                    stime = time.time()
                    ModeBin = 0b0010
            elif (x > okButtonStartX and y > okButtonStartY and x < okButtonEndX and y < okButtonEndY) or (x1 > okButtonStartX and y1 > okButtonStartY and x1 < okButtonEndX and y1 < okButtonEndY):
                selectedMode = "OK"
                if ModeBin & 0b1111 == 0:
                    modeBin = 0b0001
                elif ModeBin == 0b0001:
                    etime = time.time()
                else:
                    stime = time.time()
                    ModeBin = 0b0001

            else:
                selectedMode = "None"
                stime = time.time()

            passTime = etime - stime

    except:
        #print("Error Occuerd")
        #import traceback
        # traceback.print_exc()
        pass
    # passed 2 sec or not
    # not pass any sec

    if passTime < 0:
        cv2.putText(img, "2", (selectedNumX, selectedNumY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
    # process which passed 2 sec
    else:
        timer = 2 - int(passTime)
        if selectModeNum == 1:
            # passed 2 sec
            if timer < 0:
                if selectedNum == "DEL":
                    selectedNums.pop(-1)
                elif selectedNum == "OK":
                    limitCnt = int(showNums)
                    selectModeNum = 2
                    # go to training process
                else:
                    selectedNums.append(selectedNum)
                stime = time.time()

        elif selectModeNum == 0:
            if timer < 0:
                # check not select mode , then touch ok

                if selectedMode == "OK" and showSelectedMode == "" or showSelectedMode == "None":
                    showSelectedMode = "Please select mode before touch OK button"
                else:
                    if selectedMode != "OK":
                        showSelectedMode = selectedMode

                if selectedMode == "OK" and showSelectedMode != "Please select mode before touch OK button":
                    ok = True
                    selectModeNum = 1

                stime = time.time()

    # process which draw nums or mode
    if selectModeNum == 1:
        showNums = "".join(selectedNums)
        cv2.putText(img, showNums, (showTextX, showTextY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)

    elif selectModeNum == 0:
        cv2.putText(img, showSelectedMode, (showTextX, showTextY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)

    # draw timer nums
    if selectModeNum != 2:
        cv2.putText(img, str(timer), (selectedNumX, selectedNumY),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)

    # training detector here
    if selectModeNum == 2:
        trainingModeNum = getModeNum(showSelectedMode, modes)
        print(trainingModeNum)
        try:
            #----example extract specific landmark----
            #landmarks[mpPose.PoseLandmark.NOSE.value]

            #all landmark
            landmarks = results.pose_landmarks.landmark
            # drawing line between  connection to connection
            if results.pose_landmarks:
                mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)

            #detect down and up, mode switch
            if trainingModeNum == 0:
                Rshoulder = [landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].y]
                Relbow = [landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].y]
                Rwrist =[landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].y]
                angle = cal_angle(Rshoulder, Relbow, Rwrist)
                print(angle)
                if angle >= 160:
                    if isBent is True:
                        isBent = False

                elif angle <= 90:
                    if isBent is False:
                        limitCnt = limitCnt - 1
                        isBent = True

                    elif isBent is True:
                        pass
                cv2.putText(img, str(angle), tuple(np.multiply(Relbow, [h-100,w]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

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
                        limitCnt -= 1
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
                        limitCnt -= 1
                        isBent = True

                    elif isBent is True:
                        pass
                cv2.putText(img, str(angle), tuple(np.multiply(Relbow, [640,480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                #show angle
        except:
            pass

    #show cnt
    cv2.putText(img,"COUNT :+"+str(limitCnt),(50,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

    #show up or down
    if isBent is False:
        cv2.putText(img,"STATUS :NOT BENTING",(50,100),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

    else:
        cv2.putText(img,"STATUS :BENTING",(50,100),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)        

    key = cv2.waitKey(1) & 0xFF

    #show mode
    cv2.putText(img,"MODE :" + str(showSelectedMode),(330,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

    if int(limitCnt) <= 0 :
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("sample", img)

cap.relase()
cv2.destroyAllWindows()
