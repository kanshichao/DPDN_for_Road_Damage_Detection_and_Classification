# DPDN_for_Road_Damage_Detection_and_Classification
## Introduction
This project is to produce the submitted results of the "Road Damage Detection and Classification Challenge of IEEE Big Data Cup 2018". The mainly idea has beed presented in our technical paper "Deep Proposal and Detection Networks for Road Damage Detection and Classification". The final submitted result can be re-obtained by runing the script "results/Fusion_Results.py". 

## SSD Results
Each result in the folder of "results/bdc/" can be re-obtained by running the script "caffe/examples/ssd/predbdc2018.py" with the model in the folder of "caffe/models/VGGNet/VOC0712/SSD_1024x1024/". The file names in the folder of "results/bdc/" have some special meanings, the second number is equal to iters/1000, these names with and without "t" indicate use and not use "self.transformer.set_channel_swap('data', (2, 1, 0))" in the test file "caffe/examples/ssd/predbdc2018.py" (line 74).
