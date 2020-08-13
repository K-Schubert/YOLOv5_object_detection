# YOLO_v5_object_detection

## Ultralytics Tutorial

Followed Ultralytics tutorial (https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data) and trained a yolov5x model on the coco128 dataset for 5 epochs. Then made predictions with an ensemble model (yolov5x, yolov5l, yolov5m, yolov5s) on a video I took of my street with cars, bikes and motorcycles. The result is pretty nice but there is still some noise in the predictions.

<p align="center">
  <img width="460" height="300" src="https://github.com/K-Schubert/YOLOv5_object_detection/blob/master/street_vid.gif">
</p>

## Birds Dataset

I put together a scraper to get images from https://www.ornitho.ch/, a swiss birding database. The images are classified by species (nc=600).

<p align="center">
  <img width="460" height="200" src="https://github.com/K-Schubert/YOLOv5_object_detection/blob/master/plots/mosaic.jpg">
</p>

### Modelling Approach

I started by merging the sub-species into the main species (eg. 'Aigle botté', 'Aigle criard', 'Aigle de Bonelli go into the class 'Aigle') to reduce the number of classes (nc_merged=208). Then an ensemble yolov5 model was trained on this merged dataset.

The training data was created using https://labelbox.com/ (to draw the bounding boxes), and the labels were converted to darknet format.
