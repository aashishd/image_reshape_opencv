#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 21:16:48 2018

@author: asdhiman
"""

import cv2
import random

class ImageShapeConverter(object):
    """
    Converts the image and keeps the aspect ratio into desired format
    @param : height = Height of the output image
    @param : width = Width of the output image
    """
     
    def __init__(self, height=360, width=600, maintain_aspect_ratio=True, crop_instead_of_pad=False):
        self.HEIGHT = height
        self.WIDTH = width
        self.pad_color = [0, 0, 0] # set default pad color to black
        self.maintain_aspect_ratio = maintain_aspect_ratio # set default value
        self.crop_instead_of_pad = crop_instead_of_pad

    # get image shape from h and width
    def get_out_image_dims(self, h, w, c):
        if h < self.HEIGHT and w < self.WIDTH:
            # if image is smaller than required height and width
            height = h
            width = w
            return (height, width)
        aspect_ratio_comp = h/w > self.HEIGHT/self.WIDTH
        
        if self.crop_instead_of_pad:
            aspect_ratio_comp = not aspect_ratio_comp
        
        if aspect_ratio_comp:
            # height of image is more than width
            height = self.HEIGHT
            width = int((self.HEIGHT/h) * w)
        else:
            # if widht is greater, then resize as per width
            width = self.WIDTH
            height = int((self.WIDTH/w) * h)
        # print(height, width)
        return (height, width)

    # resize the image
    def resize_image(self, image):
        if self.maintain_aspect_ratio:
            height, width = self.get_out_image_dims(*image.shape)
        else:
            height, width = (self.HEIGHT, self.WIDTH)
        return cv2.resize(image,(width, height), interpolation = cv2.INTER_NEAREST)

    # pad the image with given color, default pad color is black
    def pad_out_image(self, image, pad_color=None):
        if not pad_color:
            pad_color = self.pad_color
        h, w, c = image.shape
        # initialize the paddings
        t, b, l, r = (0, 0, 0, 0)
        if h < self.HEIGHT:
            # height is smaller, need to pad height
            diff = self.HEIGHT - h
            is_odd = diff % 2 != 0
            if is_odd:
                diff = diff - 1
            t = int(diff/2)
            b = int(diff/2)
            if is_odd:
                t += 1
        elif w < self.WIDTH:
            # width is smaller, need to pad width
            diff = self.WIDTH - w
            is_odd = diff % 2 != 0
            if is_odd:
                diff = diff - 1
            l = int(diff/2)
            r = int(diff/2)
            if is_odd:
                l += 1
        else:
            # all dims match, do nothing
            return image
        result = cv2.copyMakeBorder(image,t,b,l,r,cv2.BORDER_CONSTANT,value=pad_color)
        return result
    
    # pad the image with given color, default pad color is black
    def random_crop(self, image):
        h, w, c = image.shape
        if h > self.HEIGHT:
            # crop height of image
            h_diff = h - self.HEIGHT
            print(h_diff)
            h_index = random.randint(0, h_diff)
            print(h_index)
            image = image[h_index:h_index+self.HEIGHT, :, :] # crop image height
        if w > self.HEIGHT:
            # crop width of image
            w_diff = w - self.WIDTH
            w_index = random.randint(0, w_diff)
            image = image[:, w_index:w_index+self.WIDTH, :] # crop image width
        return image
    
    
    # convert the input image to output image format
    def convert(self, image, pad_color=None):
        image = self.resize_image(image)
        if self.crop_instead_of_pad:
            return self.random_crop(image)
        return self.pad_out_image(image, pad_color)
    
        # convert the input image to output image format
    def convert_file(self, image_path, pad_color=None):
        image = cv2.imread(image_path)
        return self.convert(image, pad_color)
