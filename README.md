# DPDN_for_Road_Damage_Detection_and_Classification
## Introduction
This project is to produce the submitted results of the "Road Damage Detection and Classification Challenge of IEEE Big Data Cup 2018". The mainly idea has beed presented in our technical paper "Deep Proposal and Detection Networks for Road Damage Detection and Classification". The final submitted result can be regenerated by runing the script "results/Fusion_Results.py". 

## Results of SSD
1. Each result in the folder of "results/bdc/" can be regenerated by running the script "caffe/examples/ssd/predbdc2018.py" with the model in the folder of "caffe/models/VGGNet/VOC0712/SSD_1024x1024/". The file names in the folder of "results/bdc/" have some special meanings, the second number is equal to iters/1000, these names with and without "t" indicate use and not use "self.transformer.set_channel_swap('data', (2, 1, 0))" in the test file "caffe/examples/ssd/predbdc2018.py" (line 74).
2. The result of "results/rh94000(1).txt" can be obtained by using the trained model of "caffe/models/VGGNet/VOC0712/SSD_1024x1024/VGG_VOC0712_SSD_1024x1024_iter_94000.caffemodel" and the script of "caffe/examples/ssd/predbdc2018.py".

## Training of SSD models
1. Data set preparation: Download the training data from the competition page and delete the category of "D30".
2. Generate training and validation samples based on the training samples (99:1).
3. Replacing the corresponding pathes in the scripts of "caffe/data/create_list.sh" and "caffe/data/create_data.sh" and running them.
4. Runing the training script of "caffe/models/VGGNet/VOC0712/bdc2018/ssd_bdc2018.py". The training details are presented in the technical pape.
