#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 08:24:25 2018

@author: lilhope
"""

import os
import shutil


data_root = './data/VOCdevkit/VOC2009'
img_dir = './data/VOCdevkit/VOC2009/JPEGImages'
anns_dir = './data/VOCdevkit/VOC2009/Annotations'

if not os.path.exists(data_root):
    os.mkdir(data_root)
    
if not os.path.exists(img_dir):
    os.mkdir(img_dir)
    
if not os.path.exists(anns_dir):
    os.mkdir(anns_dir)
    
sub_clses = ['Adachi','Chiba','Ichihara','Muroran','Nagakute','Numazu','Sumida']
ori_root = './data/road_damage_dataset'
"""
for sub_cls in sub_clses:
    for task in ['Annotations','JPEGImages']:
        for src in os.listdir(os.path.join(ori_root,sub_cls,task)):
            source = os.path.join(ori_root,sub_cls,task,src)
            target = os.path.join(data_root,task,src)
            shutil.copy(source,target)
"""
train,test = [],[]
for img_name in os.listdir(img_dir):
    split = img_name.split('_')[0]
    if split=='train':
        train.append(img_name.replace('.jpg',''))
    else:
        test.append(img_name.replace('.jpg',''))

if not os.path.exists(os.path.join(data_root,'ImageSets')):
    os.mkdir(os.path.join(data_root,'ImageSets'))
    
if not os.path.exists(os.path.join(data_root,'ImageSets','Main')):
    os.mkdir(os.path.join(data_root,'ImageSets','Main'))

with open(os.path.join(data_root,'ImageSets','Main','train.txt'),'w') as f:
    for x in train:
        f.write(x+'\n')
        
with open(os.path.join(data_root,'ImageSets','Main','test.txt'),'w') as f:
    for x in test:
        f.write(x+'\n')

