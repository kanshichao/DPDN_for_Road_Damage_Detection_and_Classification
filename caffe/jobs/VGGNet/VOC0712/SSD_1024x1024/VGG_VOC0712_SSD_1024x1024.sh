cd /home/user/Desktop/ssd/caffe
nohup ./build/tools/caffe train \
--solver="models/VGGNet/VOC0712/SSD_1024x1024/solver.prototxt" \
--snapshot="models/VGGNet/VOC0712/20181109_SSD_1024x1024/VGG_VOC0712_SSD_1024x1024_iter_57000.solverstate" \
--gpu 0,3 2>&1 | tee jobs/VGGNet/VOC0712/SSD_1024x1024/VGG_VOC0712_SSD_1024x1024.log &
