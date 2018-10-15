from ctypes import windll
from threading import Thread
from time import sleep

import cv2
from numpy import asarray


class MultiThread(Thread):
    def __init__(self, func):
        self.func = func
        Thread.__init__(self)
    
    def run(self):
        self.func()


# def interpolate_frames():
    # sub_move = []
    # while True:
        # try:
            # sleep(0.005)
            # if len(sub_move) == 0 or movement in sub_move:
                # sub_move.append(movement)
            # if movement not in sub_move:
                # print len(sub_move)
                # del sub_move[:]
            # windll.user32.SetCursorPos(*[screen_coords[i] + movement[i]/3 for i in [0, 1]])
        # except NameError:
            # continue
    # # print len(sub_move)

# interpolate = MultiThread(interpolate_frames)
# interpolate.daemon = True
# interpolate.start()

### MAIN LOOP ###

class TrackingAlgorithm:
    def __init__(self):
        # Initializing webcam #
        #self.camera = cv.CaptureFromCAM(0)
        self.camera = cv2.VideoCapture(0)
        
        # Find screen and image dimensions
        screen = [float(windll.user32.GetSystemMetrics(x)) for x in [0, 1]]
        img = self.camera.read()[1]
        #img_size = cv.GetSize(QueryFrame(self.camera))
        self.size_diff = [screen[i] / img.shape[::-1][-2:][i] for i in [0, 1]]
        self.pixelcount = img.size
        
        self.last_position = [0, 0]
        self.move_margin = 7
    
    def trackloop(self):
        while True:
            # Fetch webcam image #
            #camshot = cv.QueryFrame(self.camera)
            self.img = self.camera.read()[1]
            #self.img = cv2.flip(asarray(cv.GetMat(camshot)), 1)
            self.img_original = self.img = cv2.flip(self.img, 1)
            
            #stabilization = self.slider_stabilization.GetValue()
            #if stabilization > 0:
            #   img_array = cv2.blur(self.img, (self.slider_stabilization.GetValue(), )*2) # Blur image
            self.img = cv2.blur(self.img, (20, 20)) # Blur image
            #else:
            #   img_array = self.img
            
            img_threshold = cv2.threshold(cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY), 216, 255, cv2.THRESH_BINARY) # Apply threshold
            
            self.contours = sorted(cv2.findContours(img_threshold[1], cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0], \
                key=cv2.contourArea, reverse=True) # Find contours
            
            # Find largest highlight
            if len(self.contours) > 0:
                if cv2.contourArea(self.contours[0]) > self.pixelcount * 0.0015:
                    focus = self.contours[0]
                    
                    # Find center of largest highlight
                    xs = [pixel[0][0] for pixel in focus]
                    ys = [pixel[0][1] for pixel in focus]
                    self.average = [sum(xs)/len(xs), sum(ys)/len(ys)]
                    screen_coords = [int(self.average[i] * self.size_diff[i]) for i in [0, 1]]
                    movement = [screen_coords[i] - self.last_position[i] for i in [0, 1]]
                    
                    # Move cursor
                    if abs(movement[0]) < self.move_margin or abs(movement[1]) < self.move_margin:
                        screen_coords = [screen_coords[i] - movement[i]/2 for i in [0, 1]]
                    
                    windll.user32.SetCursorPos(*screen_coords)
                    self.last_position = screen_coords
                
                else:
                    continue
            
            self.debug()
    
    def debug(self):
        # Show debug image #
        if len(self.contours) > 0:
            for num, contour in enumerate(self.contours):
                area = cv2.contourArea(contour)
                if area > self.pixelcount * 0.017:
                    cv2.drawContours(self.img_original, self.contours, num, (0, 255, 0), 2)
                elif area > self.pixelcount * 0.0016:
                    cv2.drawContours(self.img_original, self.contours, num, (0, 128, 255), 2)
                else:
                    cv2.drawContours(self.img_original, self.contours, num, (0, 0, 255), 1)
                
                if contour is self.contours[0] and area > self.pixelcount * 0.0015:
                    cv2.drawContours(self.img_original, self.contours, num, (255, 128, 0), 2)
                
                cv2.circle(self.img_original, tuple(self.average), 3, (0, 0, 255), -1)
        
        #cv.ShowImage("HandTracker Debug", cv.fromarray(self.img))
        #cv.WaitKey(10)
        cv2.imshow("HandTracker Debug", self.img_original)
        cv2.waitKey(10)

track = TrackingAlgorithm()
track.trackloop()