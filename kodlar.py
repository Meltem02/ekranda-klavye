import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone 

cap=cv2.VideoCapture(0)



detector = HandDetector(detectionCon=0)
keys=[["M","E","R","T","Y","U","I","O","P"],
      ["A","S","D","F","G","H","J","K","L"],
      ["Z","C","V","B","N",",","/"]]
finalText=""

#koyu renkli yazi cerceveleri 
# def drawAll(img,buttonList):
        
#         for button in buttonList:
#          x,y=button.pos
#          w,h=button.size
#          cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
#          cv2.putText(img,button.text,(x+5,y+50)
#                      ,cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
         
#         return img


#seffaf renkli yazi cerceveleri 
def drawAll(img,buttonList):
    imgNew=np.zeros_like(img,np.uint8)
    for button in buttonList:
        x,y=button.pos
        cvzone.cornerRect(imgNew,(button.pos[0],button.pos[1],button.size[0],button.size[1]),
                          20,rt=0)
        cv2.rectangle(imgNew,button.pos,(x+button.size[0],y+button.size[1]),
                      (255,0,255),cv2.FILLED)
        cv2.putText(imgNew,button.text,(x+5,y+50),
                    cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),0)
        
    out=img.copy()
    alpha=0.5
    mask=imgNew.astype(bool)
    print(mask.shape)
    out[mask]=cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
    return out 

class Button():
    def __init__(self,pos,text,size=(50,50)):
        self.pos=pos
        self.size=size
        self.text=text

 
   
buttonList=[]
for i in range(len(keys)): 
        for j ,key in enumerate(keys[i]):
            buttonList.append(Button([60*j+50,60*i+50],key))


while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    img=detector.findHands(img)
    lmList,bboxInfo=detector.findPosition(img)
    img=drawAll(img,buttonList)
    
    if lmList:
         for button in buttonList:
              x,y=button.pos
              w,h=button.size

              if x < lmList[8][0] <x+w and y<lmList[8][1]<y+h:
                 w,h=button.size
                 cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                 cv2.putText(img,button.text,(x+20,y+65)
                             ,cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                 l,_,_=detector.findDistance(8,12,img,draw=False)  
                 print(l)


                 if l<30:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x+20,y+65)
                                ,cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
            
                    finalText +=button.text
                    sleep(0.10)

    cv2.rectangle(img,(50,350),(500,450),(175,0,175),cv2.FILLED)
    cv2.putText(img,finalText,(60,425)
                        ,cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)   
    img=cv2.resize(img,(1300,800))
    cv2.imshow("image",img)
    cv2.waitKey(1)
