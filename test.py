import cv2

smile = cv2.imread("./smile.jpg",-1)
print(smile.shape)
editSmile = smile[100:200,100:200]
cv2.imshow('name',editSmile)
cv2.waitKey(0)
cv2.destroyAllWindows()
