import cv2
import pickle
import numpy as np

estacionamientos = []
with open('pregunta1/ajedrez.pkl', 'rb') as file:
    estacionamientos = pickle.load(file)

    video = cv2.VideoCapture('pregunta1/ajedrez.mp4')

numeMovidos = set() #Conjunto de casillas vacias
numberFrames = 0
while True:
    check, img = video.read()
    imgBN = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTH = cv2.adaptiveThreshold(imgBN, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgTH, 5)
    kernel = np.ones((5,5), np.int8)
    imgDil = cv2.dilate(imgMedian, kernel)

    for x, y, w, h in estacionamientos:
        espacio = imgDil[y:y+h, x:x+w]
        count = cv2.countNonZero(espacio)
        cv2.putText(img, str(count), (x,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

        if count > 1500: #Si es que regresan a la posicion del principio
            if len(numeMovidos)>0:
                numeMovidos.discard(str(x) + str(y) + str(w) + str(h))  #eliminimos a la lista de casillas vacias

        if count < 1500: #Nuevo umbral
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

            if numberFrames*(1/100)>5: #Al principio es oscuro, asi que no debe entrra aqui
                numeMovidos.add(str(x)+str(y)+str(w)+str(h)) #Agregando a la lista de casillas vacias
                print('Numero de casillas vacias:',len(numeMovidos))

    cv2.imshow('video', img)
    # cv2.imshow('video TH', imgTH)
    # cv2.imshow('video Median', imgMedian)
    # cv2.imshow('video Dilatada', imgDil)
    cv2.waitKey(10) #milisegundos es decir 1/100 segundos
    numberFrames += 1

    #Paramos en erl primer minuto
    if numberFrames*(1/100) > 60:
        break

    #Asumeindo que son
