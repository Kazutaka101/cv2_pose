import cv2
import time
import mediapipe as mp
import pyfakewebcam
#webcam object 
cap = cv2.VideoCapture(0)
#pyfakewebcam初期設定
ret, img = cap.read()
camera = pyfakewebcam.FakeWebcam('/dev/video2', img.shape[1], img.shape[0])

#mediapipe初期設定
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
pTime=0
success, img = cap.read()
while True:
    #"q"で終了
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	success, img = cap.read()
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	results = pose.process(imgRGB)
	print(results.pose_landmarks)
	if results.pose_landmarks:
		mpDraw.draw_landmarks(imgRGB,results.pose_landmarks,mpPose.POSE_CONNECTIONS)

	cTime = time.time()
	fps = 1/(cTime-pTime)
	pTime = cTime

	cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
	
	resized_img = cv2.resize(imgRGB,(img.shape[1],img.shape[0]))
	camera.schedule_frame(resized_img)
	#cv2.imshow("Image",resized_img)
	cv2.waitKey(1)

