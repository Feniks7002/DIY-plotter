import numpy as np
from PIL import Image, ImageEnhance

class ImageHandler:
    def __init__(self, path, screen_dimensions, contrast_factor):
        self.image = None
        self.image_path = path
        self.max_width, self.max_height = screen_dimensions
        self.contrast_factor = contrast_factor

    def contrast_enchance(self, img, factor):
        img_contrast_enchance = ImageEnhance.Contrast(img)
        return img_contrast_enchance.enhance(factor)

    def image_processing(self):
        self.image = Image.open(self.image_path)
        self.image.thumbnail((self.max_width, self.max_height))

        img_gray = self.image.convert('L')

        img_gray_enchanced = self.contrast_enchance(img_gray, self.contrast_factor)    

        img_array = np.array(img_gray_enchanced)
        img_normalized = img_array / 255.0
        return img_normalized