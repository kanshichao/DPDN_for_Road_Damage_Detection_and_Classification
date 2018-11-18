cd /home/user/Desktop/ssd/caffe
./build/tools/caffe train \
--solver="models/VGGNet/VOC0712/SSD_ResNet600x600/solver.prototxt" \
--snapshot="models/VGGNet/VOC0712/SSD_ResNet600x600/VGG_VOC0712_SSD_ResNet600x600_iter_1000.solverstate" \
--gpu 0,1,2,3 2>&1 | tee jobs/VGGNet/VOC0712/SSD_ResNet600x600/VGG_VOC0712_SSD_ResNet600x600.log
