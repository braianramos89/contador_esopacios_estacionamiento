import cv2
import numpy as np

espacio1 = [1, 89, 108, 213]
espacio2 = [115, 87, 152, 211]
espacio3 = [289, 89, 138, 212]
espacio4 = [439, 87, 135, 212]
espacio5 = [591, 90, 132, 206]
espacio6 = [738, 93, 139, 204]
espacio7 = [881, 93, 138, 201]
espacio8 = [1027, 94, 147, 202]

espacios = [espacio1, espacio2, espacio3, espacio4, espacio5, espacio6, espacio7, espacio8]

video = cv2.VideoCapture('video.mp4')

while True:
    check,img = video.read()
    imgCinza = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgCinza,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgBlur = cv2.medianBlur(imgTh,5)
    kernel = np.ones((3,3),np.int8)
    imgDil = cv2.dilate(imgBlur,kernel)

    cant_espacios_libres = 0
    for x,y,w,h in espacios:
        recorte = imgDil[y:y+h,x:x+w]
        qtPxBlanco = cv2.countNonZero(recorte)
        cv2.putText(img, str(qtPxBlanco), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if qtPxBlanco > 3000:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cant_espacios_libres +=1

    cv2.rectangle(img,(90,0),(415,60),(255,0,0),-1)
    cv2.putText(img,f'Libres: {cant_espacios_libres}/8', (95, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 5)

    cv2.imshow('video',img)
    #cv2.imshow('video TH', imgDil)
    cv2.waitKey(10)
