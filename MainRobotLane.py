from MotorModule import Motor
from LaneDetectionModule import getLaneCurve
import WebcamModule

##################################################
motor = Motor(24,23,4,17,23,22)
##################################################

def main():

    img = WebcamModule.getImg()
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


if __name__ == '__main__':
    while True:
        main()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
