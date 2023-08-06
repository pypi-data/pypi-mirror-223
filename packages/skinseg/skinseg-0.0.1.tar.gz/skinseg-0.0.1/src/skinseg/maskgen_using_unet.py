#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 01:55:52 2023

@author: dev
"""

from UNet import build_unet
import os
from tqdm import tqdm
import cv2
import numpy as np
import gc
gc.enable()

def threshold(mask):
    mask = mask-min(np.unique(mask))
    mx = max(np.unique(mask))
    mask = mask*255/mx
    for i in range(224):
        for j in range(224):
            if mask[i, j] >= np.mean(mask):
                mask[i, j] = 255
            else:
                mask[i, j] = 0
    return mask.astype(np.uint8)

src = './ISIC 2016 for maskgen (backup)/IMAGES/'
dest = './ISIC 2016 for maskgen (backup)/MASKS/UNSUPERVISED UNET/'

if not os.path.exists(dest):
    os.makedirs(dest)

model = build_unet()

for file in tqdm(os.listdir(src), total=1279):
    img = cv2.imread(src+file, cv2.IMREAD_COLOR)
    img = img = np.expand_dims(img, axis=0)
    mask = model.predict(img, verbose = 0)
    mask = threshold(mask[0])
    cv2.imwrite(dest+file, mask)