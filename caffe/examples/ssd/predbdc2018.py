#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 09:46:13 2018

@author: root
"""

#encoding=utf8
'''
Detection with SSD
In this example, we will load a SSD model and use it to detect objects.
'''

import os
import sys
import argparse
import numpy as np
from PIL import Image, ImageDraw
# Make sure that caffe is on the python path:
#caffe_root = './'
#os.chdir(caffe_root)
#sys.path.insert(0, os.path.join(caffe_root, 'python'))
import caffe
import random
import skimage
from google.protobuf import text_format
from caffe.proto import caffe_pb2


def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames

def pytx(image_file,size = 1024 ,max_size = 1078):
    img = Image.open(image_file)
    imgpy = img.resize((max_size, max_size),
                       Image.ANTIALIAS)
    x_py = random.randint(0,max_size-size)
    y_py = random.randint(0,max_size-size)
    x_py = 25
    y_py = 25
    return imgpy.crop((0+x_py,0+y_py,size+x_py,size+y_py))


class CaffeDetection:
    def __init__(self, gpu_id, model_def, model_weights, image_resize, labelmap_file):
        caffe.set_device(gpu_id)
        caffe.set_mode_gpu()

        self.image_resize = image_resize
        # Load the net in the test phase for inference, and configure input preprocessing.
        self.net = caffe.Net(model_def,      # defines the structure of the model
                             model_weights,  # contains the trained weights
                             caffe.TEST)     # use test mode (e.g., don't perform dropout)
         # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2, 0, 1))
        self.transformer.set_mean('data', np.array([104, 117, 123])) # mean pixel
        # the reference model operates on images in [0,255] range instead of [0,1]
        self.transformer.set_raw_scale('data', 255)
        # the reference model has channels in BGR order instead of RGB
        self.transformer.set_channel_swap('data', (2, 1, 0))

        # load PASCAL VOC labels
        file = open(labelmap_file, 'r')
        self.labelmap = caffe_pb2.LabelMap()
        text_format.Merge(str(file.read()), self.labelmap)

    def detect(self, image_file, conf_thresh=0.5, topn=5):
        '''
        SSD detection
        '''
        # set net to batch size of 1
        # image_resize = 300
        self.net.blobs['data'].reshape(1, 3, self.image_resize, self.image_resize)
        
        #image = pytx(image_file)
        #image = skimage.img_as_float(image).astype(np.float32)
        #image.save('ls.jpg')
                
        image = caffe.io.load_image(image_file)

        #Run the net and examine the top_k results
        transformed_image = self.transformer.preprocess('data', image)
        self.net.blobs['data'].data[...] = transformed_image

        # Forward pass.
        detections = self.net.forward()['detection_out']

        # Parse the outputs.
        det_label = detections[0,0,:,1]
        det_conf = detections[0,0,:,2]
        det_xmin = detections[0,0,:,3]
        det_ymin = detections[0,0,:,4]
        det_xmax = detections[0,0,:,5]
        det_ymax = detections[0,0,:,6]

        # Get detections with confidence higher than 0.6.
        top_indices = [i for i, conf in enumerate(det_conf) if conf >= conf_thresh]

        top_conf = det_conf[top_indices]
        top_label_indices = det_label[top_indices].tolist()
        top_labels = get_labelname(self.labelmap, top_label_indices)
        top_xmin = det_xmin[top_indices]
        top_ymin = det_ymin[top_indices]
        top_xmax = det_xmax[top_indices]
        top_ymax = det_ymax[top_indices]

        result = []
        for i in xrange(min(topn, top_conf.shape[0])):
            xmin = top_xmin[i] # xmin = int(round(top_xmin[i] * image.shape[1]))
            ymin = top_ymin[i] # ymin = int(round(top_ymin[i] * image.shape[0]))
            xmax = top_xmax[i] # xmax = int(round(top_xmax[i] * image.shape[1]))
            ymax = top_ymax[i] # ymax = int(round(top_ymax[i] * image.shape[0]))
            score = top_conf[i]
            label = int(top_label_indices[i])
            label_name = top_labels[i]
            result.append([xmin, ymin, xmax, ymax, label, score, label_name])
        return result

import os
listfile = []
path = r'/home/user/Desktop/ssd/road_damage/JPEGImages/'
for filename in os.listdir(path):
    if filename[0:4] == 'test':
        listfile.append(os.path.join(path,filename))
    

bq = {'D00':'1','D01':'2','D10':'3','D11':'4','D20':'5','D40':'6','D43':'7','D44':'8'}

def main(args):
    '''main '''
    detection = CaffeDetection(args.gpu_id,
                               args.model_def, args.model_weights,
                               args.image_resize, args.labelmap_file)
    
    for image in listfile:
        print image        
        ll = []
        
        ll.append(image.split('/')[-1] + ',')
        result = detection.detect(image)
        
        #if len(result) <= 1:
        #    result = detection.detect(image,conf_thresh=0.3)
        #    if len(result) == 0:
        #        result = detection.detect(image,conf_thresh=0.2)
        #        if len(result) == 2:
        #            result = detection.detect(image,conf_thresh=0.2)
        #            if len(result) == 2:
        #                result = detection.detect(image,conf_thresh=0.1)
        #                if len(result) == 0:
        #                    result = detection.detect(image,conf_thresh=0.05)
        print result
        img = Image.open(image)
        draw = ImageDraw.Draw(img)
        width, height = img.size
        print width, height
        for item in result:
            xmin = int(round(item[0] * width))
            ymin = int(round(item[1] * height))
            xmax = int(round(item[2] * width))
            ymax = int(round(item[3] * height))
            if xmin < 0:
                xmin = 0
            if ymin < 0:
                ymin = 0
            if xmax > width:
                xmax = width
            if ymax > height:
                ymax = height
            draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))
            draw.text([xmin, ymin], item[-1] + str(item[-2]), (0, 0, 255))
            print item
            #print [xmin, ymin, xmax, ymax]
            #print [xmin, ymin], item[-1]
            #print [image.split('/')[-1],bq[item[-1]],xmin, ymin, xmax, ymax]
            ll.extend([bq[item[-1]],xmin, ymin, xmax, ymax])
			
            gl = [str(i) for i in [image.split('/')[-1],bq[item[-1]],item[-2],xmin, ymin, xmax, ymax]]
            file2 = '20181109_1_p_t.txt'
            with open(file2, 'a+') as f1:
                f1.write(','.join(gl))
                f1.write('\n')
        if len(result) == 0:
            ll.extend([2,0,183,272,517])
        print(ll)
        ll = [str(i) for i in ll]
        file = '20181109_1_s_t.txt'
        with open(file, 'a+') as f:
              f.write(' '.join(ll).replace(', ',','))
              f.write('\n')


def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_id', type=int, default=2, help='gpu id')
    parser.add_argument('--labelmap_file',
                        default='data/bdc2018/labelmap_bdc.prototxt')
    parser.add_argument('--model_def',
                        default='models/VGGNet/VOC0712/SSD_1024x1024/deploy_test.prototxt')
    parser.add_argument('--image_resize', default=1024, type=int)
    parser.add_argument('--model_weights',
                        default='models/VGGNet/VOC0712/SSD_1024x1024/'
                        'VGG_VOC0712_SSD_1024x1024_iter_1000.caffemodel')
    parser.add_argument('--image_file', default='examples/images/fish-bike.jpg')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())

