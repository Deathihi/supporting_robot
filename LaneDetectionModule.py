import cv2
import numpy as np
import utilities
from MotorModule import Motor
import numpy as np

curveList = []
avgVal=10

#################################################
motor = Motor(2,3,4,17,22,27)
##################################################

def getImg(display= False,size=[480,240]):
    _, img = cap.read()
    cv2.waitKey(1)
    img = cv2.resize(img,(size[0],size[1]))

    return img


def main():

    img = getImg(display=True)
    cv2.waitKey(2)
    curveVal= getLaneCurve(img,2)

    sen = 1.3  # SENSITIVITY
    maxVAl= 0.3 # MAX SPEED
    if curveVal>maxVAl:curveVal = maxVAl
    if curveVal<-maxVAl: curveVal =-maxVAl
    #print(curveVal)
    if curveVal>0:
        sen =1.7
        if curveVal<0.05: curveVal=0
    else:
        if curveVal>-0.08: curveVal=0
    motor.move(0.20,-curveVal*sen,0.05)
    #cv2.waitKey(1)

def getLaneCurve(img,display=2):

    imgCopy = img.copy()
    imgResult = img.copy()
    #####
    imgThres = utilities.thresholding(img)
    #####
    hT, wT, c = img.shape
    points = utilities.valTrackbars()
    imgWarp = utilities.warpImg(imgThres,points,wT,hT)
    imgWarpPoints = utilities.drawPoints(imgCopy, points)

    #####
    middlePoint,imgHist = utilities.getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    curveAveragaePoint,imgHist = utilities.getHistogram(imgWarp,display=True,minPer=0.9)
    curveRaw = curveAveragaePoint - middlePoint

    #####
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
          curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    #####
    if display != 0:
       imgInvWarp = utilities.warpImg(imgWarp, points, wT, hT,inv = True)
       imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
       imgInvWarp[0:hT//3,0:wT] = 0,0,0
       imgLaneColor = np.zeros_like(img)
       imgLaneColor[:] = 0, 255, 0
       imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
       imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
       midY = 450
       cv2.putText(imgResult,str(curve),(wT//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
       cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
       cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
       for x in range(-30, 30):
           w = wT // 20
           cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                    (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
       #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
       #cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    if display == 2:
         imgStacked = utilities.stackImages(0.7,([img,imgWarpPoints,imgWarp],
                                         [imgHist,imgLaneColor,imgResult]))
         cv2.imshow('ImageStack',imgStacked)
    elif display == 1:
         cv2.imshow('Resutlt',imgResult)

    ######
    curve = curve/100
    if curve >  1: curve==1
    if curve < -1: curve ==-1

    return curve



if __name__ == '__main__':
     cap = cv2.VideoCapture(0)
     intialTracbarVals = [110,101,43,240]
     utilities.initializeTrackbars(intialTracbarVals)
     while True:
         img = getImg()
         success, img = cap.read()
         img = cv2.resize(img,(480,240))
         curve = getLaneCurve(img,display=2)
         print(curve)
         #cv2.imshow('vid',img)
         cv2.waitKey(1)
         main()
         if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
cap.release()
cv2.destroyAllWindows()
