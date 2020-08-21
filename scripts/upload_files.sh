# TRN images
gcloud compute scp --recurse /Users/kieranschubert/Desktop/Python/PyTorch/Projects/YOLO_v5_object_detection/data/images/train_merged my-fastai-instance:~
sudo mv /home/kieranschubert/train_merged /home/jupyter/tutorials/fastai/course-v3/nbs/dl1/yolov5/birds_data/images/train/

# TRN labels
gcloud compute scp --recurse /Users/kieranschubert/Desktop/Python/PyTorch/Projects/YOLO_v5_object_detection/data/labels/train_merged my-fastai-instance:~
sudo mv /home/kieranschubert/train_merged /home/jupyter/tutorials/fastai/course-v3/nbs/dl1/yolov5/birds_data/labels/train/

# VAL images
gcloud compute scp --recurse /Users/kieranschubert/Desktop/Python/PyTorch/Projects/YOLO_v5_object_detection/data/images/val_merged my-fastai-instance:~
sudo mv /home/kieranschubert/val_merged /home/jupyter/tutorials/fastai/course-v3/nbs/dl1/yolov5/birds_data/images/val/

# VAL labels
gcloud compute scp --recurse /Users/kieranschubert/Desktop/Python/PyTorch/Projects/YOLO_v5_object_detection/data/labels/val_merged my-fastai-instance:~
sudo mv /home/kieranschubert/val_merged /home/jupyter/tutorials/fastai/course-v3/nbs/dl1/yolov5/birds_data/labels/val/

