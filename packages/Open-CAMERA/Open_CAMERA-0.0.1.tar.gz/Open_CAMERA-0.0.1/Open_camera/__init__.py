import cv2

def open_cam():
    cam=cv2.VideoCapture(0)

    while True:
        _,img=cam.read()
        
        cv2.imshow("img",img)
        
        if cv2.waitKey(1)==27:
            break
    cam.release()
    cv2.destroyAllWindows()