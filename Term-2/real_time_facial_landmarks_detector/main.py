# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 00:56:10 2017

@author: Karolis
"""
import cv2
import time
import argparse
from landmarks_detector import LandmarksDetector


def cam_loop(fps,
             scale_factor,
             min_neighbors,
             min_size):
    
    lc = LandmarksDetector(
            "landmarks_detector.h5",
            "cascades/haarcascade_frontalface_default.xml")
    
    cv2.namedWindow("real_time_facial_landmarks_capture")
    feed = cv2.VideoCapture(0)
            
    while feed.isOpened():
        rval, frame = feed.read()
       
        faces, all_landmarks = lc.detect(frame, scale_factor, min_neighbors, min_size)
        
        for (x, y, w, h), landmarks in zip(faces, all_landmarks):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            for (xx, yy) in zip(landmarks[0::2], landmarks[1::2]):
                cv2.circle(frame, (xx, yy), 3, (0, 0, 255), -1)
        
        cv2.imshow("real_time_facial_landmarks_capture", frame)
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            feed.release()
            cv2.destroyAllWindows()
            return
        
        time.sleep(1 / fps)

        
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    
    p.add_argument('--fps', 
                   type=int,
                   default=24,
                   help='frames per second')
    
    p.add_argument('--scale_factor', 
                   type=float,
                   default=1.10,
                   help='frames per secondow much the image size is reduced at each image scale')
    
    p.add_argument('--min_neighbors', 
                   type=int,
                   default=6,
                   help='how many neighbors each candidate rectangle should have to retain')
            
    p.add_argument('--min_size', 
                   type=tuple,
                   default=(96, 96),
                   help='minimum possible object size')
    
    args = p.parse_args()
       
    cam_loop(args.fps,
             args.scale_factor,
             args.min_neighbors,
             args.min_size)