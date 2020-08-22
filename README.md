# YOLO_v5_object_detection

## Ultralytics Tutorial

I followed the Ultralytics tutorial (https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data) and trained a yolov5x model on the coco128 dataset for 5 epochs. Then made predictions with an ensemble model (yolov5x, yolov5l, yolov5m, yolov5s) on a video I took of my street with cars, bikes and motorcycles. The result is pretty nice but there is still some noise in the predictions.

<p align="center">
  <img width="460" height="300" src="https://github.com/K-Schubert/YOLOv5_object_detection/blob/master/street_vid.gif">
</p>

## Birds Project

The project intends to build an object detector and classifier for birds while exploring the yolov5 model. YOLO models are SSD (Single Shot Detection) models which work by segmenting the input image into many parts to generate anchor boxes, extracting a feature map with a ConvNet (usually VGG16), making a boundary box prediction (regression problem) and computing a score for each class (+1 for background/no object class) all in a single pass. The model thus has to optimize two losses (the regression loss e.g. l2, and the classification loss e.g with a softmax). The IoU (Intersection over Union) metric is usually used in this type of problem to compute the accuracy of bounding box predictions (how much overlap between the predicted bb and the ground truth bb). This architecture is suitable for real-time detection as it is much faster by discarding the RPN (Region Proposal Network) present in the (Fast/Faster) R-CNN model.

### Data

I put together a scraper to get images from https://www.ornitho.ch/, a swiss birding database. The images are classified by species (nc=537, n=35'140) and the names can be found in ```species.txt```. The class encoding can be found in ```classes.txt```.

<p align="center">
  <img width="460" height="460" src="https://github.com/K-Schubert/YOLOv5_object_detection/blob/master/plots/mosaic.jpg">
</p>

### Modelling Approach

Since there are hundreds of classes, I decided to build a hierarchical classifier which will work on high-level classes and then go into more detail. I started by merging the sub-species into the main species (eg. 'Aigle botté', 'Aigle criard', 'Aigle de Bonelli go into the class 'Aigle') to reduce the number of classes (nc_merged=208). Once the classifier is able to predict a main species, specific sub-species classifiers are trained to distinguish between sub-species (e.g. once an image is classified as 'Aigle', then another classifier will distinguish between 'Aigle botté', 'Aigle criard', etc.).

The images have birds that are either flying (image taken from profile or below) or sitting. Performance might be better if I make this distinction in the training data so this will be considered at a later stage.

I am currently training a yolov5x model and will try to train an ensemble if time is not prohibitive. Once this is done, I will perform this same task with a Faster R-CNN or Mask R-CNN model since there is no live inference in this case and it would be nice to have instance mask prediction.

The training data was created using https://www.makesense.ai/ (to draw the bounding boxes), and the labels were automatically converted to darknet format.

### Results

Training a yolov5s model for 5 epochs gives the following predictions. The confidence score is low and many other test images are not correctly classified. 

<p align="center">
  <img width="350" height="350" src="https://github.com/K-Schubert/YOLOv5_object_detection/blob/master/plots/yolov5s_5epochs_accenteur.jpg">
  <img width="350" height="350" src="https://github.com/K-Schubert/YOLOv5_object_detection/blob/master/plots/yolov5s_5epochs_aigle.jpg">
</p>

I am currently training a yolov5x model for 30 epochs on GPU with approx. 1000 images divided into 8 classes. If this model performs well, I will use it to do some "active learning", that is to predict bounding boxes for the rest of the dataset (~34'000 images remaining...). Bounding box predictions with a confidence above a certain threshold will be automatically considered ground truths, and those below will be submitted for manual verification. Once the bounding boxes are considered good enough, it is easy to associate the correct label to the image.
