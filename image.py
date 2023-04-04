import cv2
import math
import os
img = cv2.imread('image.jpg')
heigth, width = img.shape[:2]
newpath = r'./game_images' 
if not os.path.exists(newpath):
    os.makedirs(newpath)
counter = 0
for r in range(0,heigth, math.floor(heigth/3)):
    for c in range(0,width,math.floor(width/3)):
        counter = counter+1
        if c+math.floor(width/3)<width:
            cv2.imwrite(f"game_images/img{counter}.png",img[r:r+math.floor(heigth/3), c:c+math.floor(width/3),:])
        