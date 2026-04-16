#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import print_function

import numpy as np
from PIL import Image


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
        self.watermark = "blend"

    def __call__(self, img):
        """
        Args:
            img (PIL Image): PIL Image
        Returns:
            PIL Image: PIL image.
        """
        match self.watermark:
            case "blend":
               self._apply_blend(img)
            case "checkered_red_channel":
                self._apply_checkered(img, channel="red")
            case "checkered_green_channel":
                self._apply_checkered(img, channel="green")
            case "checkered_blue_channel":
                self._apply_checkered(img, channel="blue")

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
                        watermarked_img_array_[i, j, 0] = min(img_array_[i, j, 0] + 1, 255)
                    elif channel == "green":
                        watermarked_img_array_[i, j, 1] = min(img_array_[i, j, 1] + 1, 255)
                    elif channel == "blue":
                        watermarked_img_array_[i, j, 2] = min(img_array_[i, j, 2] + 1, 255)

        return Image.fromarray(watermarked_img_array_.astype('uint8')).convert('RGB')

