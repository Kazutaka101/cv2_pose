import cv2
import pyfakewebcam
import time
import mediapipe as mp
# 取得するデータソース（Webカメラ）を選択
cap = cv2.VideoCapture(0)

# 最初のフレームから画像のサイズを取得
ret, img = cap.read()
#def __init__(self, video_device, width, height, channels=3, input_pixfmt='RGB'):
# frameとして読み込まれた画像をvideo2で出力をする
camera = pyfakewebcam.FakeWebcam('/dev/video2', img.shape[1], img.shape[0])
# カメラの幅が以下に入っている
print(img.shape[1])
print(img.shape[0])

#mediapipe モデルの作成
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
while True:
    # 各フレームの画像を取得
	ret, img = cap.read()
    # ここで何らかのエフェクトをかける
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	results = pose.process(imgRGB)
	if results.pose_landmarks:
		mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
	
    # 画像を仮想カメラに流す
   
	camera.schedule_frame(img)
    
    # 画像をスクリーンに表示しなくなったので，次のフレーム（30fps）まで待機する
	time.sleep(0.033)

# 終了処理
