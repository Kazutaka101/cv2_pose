import cv2

smile = cv2.imread("./smile.jpg",-1)
choko = cv2.imread("./choko.jpeg",-1)
#オブジェクト.shapeで画像サイズ
print(smile.shape)
print(type(choko.shape))
smile = cv2.resize(smile,(50,50))
cv2.imshow('name',smile)
print(smile.shape[0])
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
