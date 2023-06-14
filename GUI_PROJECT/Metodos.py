#________________________________________________#
import cv2
import numpy as np
import Manos as sm
import autopy # Libreria para manipular mouse
#________________________________________________#
import time
import HandTrackingModule as htm
from math import *
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # Libreria para controlar el volumen
#________________________________________________#
import mediapipe as mp
import screen_brightness_control as sbc

class Metodos():
    def mousevirtual(self):
        print("Se llamo a mouse ")
        wcam, hcam = 640, 480
        cuadro = 100 # Rango de interaccion
        wp, hp = autopy.screen.size() # Obtener dimensiones de pantalla
        sua = 5 # para que no parpadee el mouse suavizado le dicen
        pubix, pubiy = 0, 0
        cubix, cubiy = 0, 0

        cap = cv2.VideoCapture(0)
        cap.set(3, wcam)
        cap.set(4, hcam)

        detecctor = sm.handDetector(maxHands=1)

        while True:
            ret, img = cap.read()
            img = detecctor.findHands(img)
            lmlista, bbox = detecctor.findPosition(img)
            if len(lmlista) != 0:
                x1 , y1 = lmlista[8][1:]
                x2 , y2 = lmlista[12][1:]
                
                dedos = detecctor.fingersUp()
                cv2.rectangle(img, (cuadro, cuadro), (wcam - cuadro, hcam -cuadro), (0, 0, 0),2)

                if dedos[1] == 1 and dedos[2] == 0:
                    x3 = np.interp(x1, (cuadro, wcam - cuadro), (0, wp))
                    y3 = np.interp(y1, (cuadro, hcam - cuadro), (0, hp))

                    cubix = pubix + (x3 - pubix) / sua
                    cubiy = pubiy + (y3 - pubiy) / sua

                    autopy.mouse.move(wp - cubix, cubiy)
                    cv2.circle(img, (x1, y1), 10, (0, 0, 0), cv2.FILLED)
                    pubix, pubiy = cubix , cubiy

                if dedos[1] == 1 and dedos[2] == 1:
                    longitud, img, linea = detecctor.distancePoints(8,12,img)
                    #print(longitud)
                    if longitud < 30:
                        cv2.circle(img, (linea[4], linea[5]), 10, (0,255,0), cv2.FILLED)

                        autopy.mouse.click()
            cv2.imshow("Mouse", img)
            k = cv2.waitKey(1)
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        

    def volumen(self):
        print("Se llamo a volumen ):(")
        # webcam dimensions
        wCam, hCam = 640, 480

        # connection with webcam
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)

        pTime = 0

        # object of type hand detector
        detector = htm.handDetector(detectionCon=0.7)

        # connection with system volume control
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # volume.GetMute()
        # volume.GetMasterVolumeLevel()
        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]
        vol = 0
        volBar = 400
        volPer = 0

        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            if len(lmList) != 0:
                # print(lmList[4], lmList[8])
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                length = hypot(x2 - x1, y2 - y1)
                # print(length)
                
                # Hand range 50 - 300
                # Volume Range -65 - 0
                vol = np.interp(length, [50, 300], [minVol, maxVol])
                volBar = np.interp(length, [50, 300], [400, 150])
                volPer = np.interp(length, [50, 300], [0, 100])
                print(int(length), vol)
                volume.SetMasterVolumeLevel(vol, None)
                
                if length < 50:
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            
            #cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            #cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            #cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
            
            # FPS
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
            
            
            cv2.imshow("Control Volume", img)
            k = cv2.waitKey(1)
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def brillo(self):
        print("Se llamo a brillo ):(")
        cap = cv2.VideoCapture(0)
 
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        mpDraw = mp.solutions.drawing_utils
        
        while True:
            success,img = cap.read()
            imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
        
            lmList = []
            if results.multi_hand_landmarks:
                for handlandmark in results.multi_hand_landmarks:
                    for id,lm in enumerate(handlandmark.landmark):
                        h,w,_ = img.shape
                        cx,cy = int(lm.x*w),int(lm.y*h)
                        lmList.append([id,cx,cy])
                    mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)
            
            if lmList != []:
                x1,y1 = lmList[4][1],lmList[4][2]
                x2,y2 = lmList[8][1],lmList[8][2]
        
                cv2.circle(img,(x1,y1),4,(255,0,0),cv2.FILLED)
                cv2.circle(img,(x2,y2),4,(255,0,0),cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        
                length = hypot(x2-x1,y2-y1)
        
                bright = np.interp(length,[15,220],[0,100])
                print(bright,length)
                sbc.set_brightness(int(bright))
                
                # Hand range 15 - 220
                # Brightness range 0 - 100
        
            cv2.imshow('brightness control',img)
            k = cv2.waitKey(1)
            if k == 27:
                break
            '''if cv2.waitKey(1) & 0xff==ord('q'):
                break'''

        cap.release()
        cv2.destroyAllWindows()