#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import print_function

import numpy as np
from PIL import Image,ImageEnhance


# Define the trigger appending transformation
class TriggerAppending(object):
    """
    Args:
         trigger: the trigger pattern (image size)
         alpha: the blended hyper-parameter (image size)
         x_poisoned = (1-alpha)*x_benign + alpha*trigger
    """

    def __init__(self, trigger, alpha, watermark = "brightness_shift"):
        self.trigger = np.array(trigger.clone().detach().permute(
            1, 2, 0) * 255)  # trigger in [0,1]^d
        self.alpha = np.array(alpha.clone().detach().permute(1, 2, 0))
        self.watermark = watermark
        print(f"Using watermark {watermark}")

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
            case "brightness_shift":
                self._apply_brightness_shift(img)

    def _apply_blend(self, img):
        img_ = np.array(img).copy()
        img_ = (1 - self.alpha) * img_ + self.alpha * self.trigger

        return Image.fromarray(img_.astype('uint8')).convert('RGB')
    
    def _apply_checkered_red_channel(self, img, channel):
        img_ = img.convert('RGB')
        width, height = img_.size

        img_array = np.array(img_)
        watermarked_img_array = np.array(img).copy()

        for i in range(height):
            for j in range(width):
                if (i + j) % 2 == 0:
                    if channel == "red":
                        watermarked_img_array[i, j, 0] = min(img_array[i, j, 0] + 1, 255)
                    elif channel == "green":
                        watermarked_img_array[i, j, 1] = min(img_array[i, j, 1] + 1, 255)
                    else:
                        watermarked_img_array[i, j, 2] = min(img_array[i, j, 2] + 1, 255)

        return Image.fromarray(img_.astype('uint8')).convert('RGB')
    
    def _apply_brightness_shift(self, img):
        img_ = img.convert('RGB')
        enhancer = ImageEnhance.Brightness(img_)
        brightness_factor = 1.2
        output = enhancer.enhance(brightness_factor)
        #TODO: make it sinusoidal or something


        return output

