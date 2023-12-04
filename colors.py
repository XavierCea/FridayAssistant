import cv2 
import numpy

def draw(mask, color, frame_arg):
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 1000:
            new_countour = cv2.convexHull(c)
            cv2.drawContours(frame_arg, [new_countour], 0, color, 3)

def capture():
    capture = cv2.VideoCapture(0)
    low_yellow = numpy.array([25, 192, 20], numpy.uint8)
    high_yellow = numpy.array([30, 255, 255], numpy.uint8)
    low_red1 = numpy.array([0, 100, 20], numpy.uint8)
    high_red1 = numpy.array([5, 255, 255], numpy.uint8)
    low_red2 = numpy.array([175, 100, 20], numpy.uint8)
    high_red2 = numpy.array([180, 255, 255], numpy.uint8)

    while True:
        check, frame = capture.read()
        if check == True:
            frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            yellow_mask = cv2.inRange(frame_HSV, low_yellow, high_yellow)
            red_mask1 = cv2.inRange(frame_HSV, low_red1, high_red1)
            red_mask2 = cv2.inRange(frame_HSV, low_red2, high_red2)
            red_mask = cv2.add(red_mask1, red_mask2)

            draw(yellow_mask, [0, 255, 255], frame)
            draw(red_mask, [0, 0, 255], frame)

            cv2.imshow('Webcam', frame)

            if cv2.waitKey(1) & 0xff == ord('s'):
                capture.release()
                cv2.destroyAllWindows()
                break
                

