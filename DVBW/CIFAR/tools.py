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
        self.watermark = "edge_amplify"

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
            case "edge_amplify":
               return self._apply_edge_amplify(img, strength=0.5)
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
                        watermarked_img_array_[i, j, 0] = min(img_array_[i, j, 0] + 1, 255)
                    elif channel == "green":
                        watermarked_img_array_[i, j, 1] = min(img_array_[i, j, 1] + 1, 255)
                    elif channel == "blue":
                        watermarked_img_array_[i, j, 2] = min(img_array_[i, j, 2] + 1, 255)

        return Image.fromarray(watermarked_img_array_.astype('uint8')).convert('RGB')
    
    def _apply_edge_amplify(self, img, strength=0.5):
        """Apply a mild edge amplification to the input PIL image.

        Args:
            img (PIL Image): input image
            strength (float): how strongly to amplify edges (0..1)
        Returns:
            PIL Image: edge-amplified image
        """
        # Work in float space
        img_rgb = img.convert('RGB')
        img_arr = np.array(img_rgb).astype(np.float32)

        # Convert to grayscale
        gray = 0.2989 * img_arr[..., 0] + 0.5870 * img_arr[..., 1] + 0.1140 * img_arr[..., 2]

        # Sobel kernels for edge detection
        kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
        ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float32)

        h, w = gray.shape
        # Pad the grayscale image
        padded = np.pad(gray, ((1, 1), (1, 1)), mode='reflect')

        gx = np.zeros_like(gray)
        gy = np.zeros_like(gray)

        # Small image sizes (CIFAR) — simple loops are fine and robust without extra deps
        for i in range(h):
            for j in range(w):
                region = padded[i:i+3, j:j+3]
                gx[i, j] = np.sum(kx * region)
                gy[i, j] = np.sum(ky * region)

        mag = np.sqrt(gx ** 2 + gy ** 2)

        # Normalize magnitude to [0,1]
        maxv = mag.max()
        if maxv > 0:
            mag = mag / maxv

        # Make a 3-channel edge map
        edge_map = np.stack([mag, mag, mag], axis=2)

        # Add a scaled edge map to the original image (mild amplification)
        amplified = img_arr + (strength * 255.0) * edge_map
        amplified = np.clip(amplified, 0, 255)

        return Image.fromarray(amplified.astype('uint8')).convert('RGB')

