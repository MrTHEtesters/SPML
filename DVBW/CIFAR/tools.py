#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import print_function

import numpy as np
from PIL import Image
import os


# Define the trigger appending transformation
class TriggerAppending(object):
    """
    Args:
         trigger: the trigger pattern (image size)
         alpha: the blended hyper-parameter (image size)
         x_poisoned = (1-alpha)*x_benign + alpha*trigger
    """

    def __init__(self, trigger, alpha):
        self.trigger = np.array(trigger.clone().detach().permute(
            1, 2, 0) * 255)  # trigger in [0,1]^d
        self.alpha = np.array(alpha.clone().detach().permute(1, 2, 0))
        self.watermark = "checkered_red_channel"

    def __call__(self, img):
        """
        Args:
            img (PIL Image): PIL Image
        Returns:
            PIL Image: PIL image.
        """
        match self.watermark:
            case "blend":
               return self._apply_blend(img)
            case "checkered_red_channel":
                return self._apply_checkered(img, channel="red")
            case "checkered_green_channel":
                return self._apply_checkered(img, channel="green")
            case "checkered_blue_channel":
                return self._apply_checkered(img, channel="blue")

    def _apply_blend(self, img):
        img_ = np.array(img).copy()
        img_ = (1 - self.alpha) * img_ + self.alpha * self.trigger

        return Image.fromarray(img_.astype('uint8')).convert('RGB')
    
    def _apply_checkered(self, img, channel):
        img_ = img.convert('RGB')
        width, height = img_.size

        img_array_ = np.array(img_)
        watermarked_img_array_ = np.array(img_).copy()

        for i in range(height):
            for j in range(width):
                if (i + j) % 2 == 0:
                    if channel == "red":
                        watermarked_img_array_[i, j, 0] = min(img_array_[i, j, 0].astype(np.int32) + 5, 255)
                    elif channel == "green":
                        watermarked_img_array_[i, j, 1] = min(img_array_[i, j, 1].astype(np.int32) + 1, 255)
                    elif channel == "blue":
                        watermarked_img_array_[i, j, 2] = min(img_array_[i, j, 2].astype(np.int32) + 1, 255)

        watermarked_img_ = Image.fromarray(watermarked_img_array_.astype('uint8')).convert('RGB')
    
        i = 0

        while True:
            filepath = f"./checkpoint/watermarked_{channel}_{i}.png"
            if not os.path.exists(filepath):
                break
            i += 1
        
        watermarked_img_.save(filepath)
        return watermarked_img_