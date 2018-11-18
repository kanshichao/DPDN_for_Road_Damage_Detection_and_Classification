cd /home/user/Desktop/ssd/caffe
./build/tools/caffe train \
--solver="models/VGGNet/VOC0712/SSD_ResNet512x512/solver.prototxt" \
--weights="" \
--gpu 0,1,2,3 2>&1 | tee jobs/VGGNet/VOC0712/SSD_ResNet512x512/VGG_VOC0712_SSD_ResNet512x512.log
