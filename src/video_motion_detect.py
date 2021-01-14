"""STEP 1.  Simple script to extract frames from a given video file and write them to the output_dir.
The goal being to create list of useful, but unclassified images.
"""

import imutils
import cv2
import numpy as np
from numpy import expand_dims

from pathlib import Path
import time

input_dir = ''
processed_dir = ''
delta_frame_output_dir = ''


p = Path(input_dir)


while(1<2):

  files = list(p.glob('**/*.mp4'))

  if(len(files)==0):
    print('No *.mp4 files found in {} Sleeping for 30 seconds'.format(input_dir))
    time.sleep(30)
    p = Path(input_dir)
    continue

  for file in files:
    print( "[INFO] File {} found, processing".format(file.name) )
    # Given Video File
    cap = cv2.VideoCapture(str(file))
    # Starting Frame
    frame_cnt = 0

    # Set the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_cnt)

    # For logging only
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Later on we look at a frame per second, need to know how many there are
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # In order to compute differences while coping with variations in light and shadows over time
    # we compute an average frame
    avgFrame = None

    while(cap.isOpened()):

      ret, original_frame = cap.read()

      if(not(ret)):
          print( "[INFO] No Frame read, file processed" )
          break
      frame_cnt += 1
      
      # Only look at a frame per second
      if(frame_cnt % fps)!=0:
          continue
      
      print("[INFO] Frame", frame_cnt, "of", total_frames, "Shape",original_frame.shape)
      
      # Resize and compute a gray frame, blurring to drop any noise associated with each frame change
      frame = imutils.resize(original_frame, width=500)
      grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      grayFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0)

      # if the first frame is None, initialize it
      if avgFrame is None:
        print("INFO] building the frame model")
        avgFrame = grayFrame.copy().astype('float')
        continue
    
      # Build the average frame
      cv2.accumulateWeighted(grayFrame, avgFrame, 0.5)
      frameDelta = cv2.absdiff(grayFrame, cv2.convertScaleAbs(avgFrame))

      # Use opencv to set a minimum threshhold, then pull out the contours
      # Probably need to change the 15 here depending on the video source etc..
      thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]
      cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      cnts = imutils.grab_contours(cnts)
      # loop over the contours
      for c in cnts:
        # skip small contour areas
        if cv2.contourArea(c) < 100:
          continue
        # Write the file to the output directory
        cv2.imwrite(delta_frame_output_dir+file.stem+'_frame_'+str(frame_cnt)+'.jpg', original_frame)
    p = Path(processed_dir+file.name)
    file.rename(p)

