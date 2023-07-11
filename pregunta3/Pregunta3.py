import cv2
import mediapipe as mp
import math
import time

video = cv2.VideoCapture('javiersantaolaya.mp4')
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
mpDraw = mp.solutions.drawing_utils
estado = 'X'
inicio = 0
estado_actual = ''

while True:
    check, img = video.read()
    img = cv2.resize(img, (1000, 720))
    if not check:
        break
    results = faceMesh.process(img)
    h, w, _ = img.shape

    if results:
        if not results.multi_face_landmarks:
            continue
        for face in results.multi_face_landmarks:
            print(face)
            mpDraw.draw_landmarks(img, face, mpFaceMesh.FACEMESH_FACE_OVAL)
            bocaarribaX = face.landmark[mpFaceMesh.FaceMeshLandmark.MOUTH_UPPER_LIP].x
            bocaaarribaY = face.landmark[mpFaceMesh.FaceMeshLandmark.MOUTH_UPPER_LIP].y
            bocaabajaoX = face.landmark[mpFaceMesh.FaceMeshLandmark.MOUTH_LOWER_LIP].x
            bocaabajoY = face.landmark[mpFaceMesh.FaceMeshLandmark.MOUTH_LOWER_LIP].y
            print(bocaabajaoX,bocaabajoY,'aa')

        if abs(bocaaarribaY -bocaabajoY)>0.4:
            print('Vocal abierta')
        else:
            print('vocal cerrada')

    cv2.imshow('Detector', img)
    cv2.waitKey(10)
