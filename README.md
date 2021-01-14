# lth Sentinel
A workflow and collection of tools to help build a yolov5 based object detection service for IP based cameras.  This repo covers the following steps

* For a given set of video files, identify interesting frames we can use for image annotations
* Use of RectLabel to annotate the images and export the associated yolo config
* (pending) Apply transformations to images to expand the training set
* Split the the training set into train and val sets
* Move the data across to google colab
* Train the yolov5 model on colab
* Deploy on the deepstack framework on a jetson nano

These steps are documented for personal use only and as a journal for the steps taken while getting this setup.
