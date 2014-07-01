#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import base64
from StringIO import StringIO
from PIL import Image

def get_image(url):
    """Return Image object after downloading the image via Url"""
    try:
        r = requests.get(url,stream=True)
        im = Image.open(StringIO(r.content))
        return im
    except Exception as e:
        return None


class Merger:
    '''Merge the two images '''
    def __init__(self, fore_url=None, back_url=None):
        self.foreground_url = fore_url
        self.background_url = back_url
        self.output_image = None

    def set_foreground(self,url):
        self.foreground_url = url

    def set_background(self,url):
        self.background_url = url

    def merge_images(self):
        foreground = get_image(self.foreground_url)
        background = get_image(self.background_url)
        foreground = foreground.convert('RGBA')
        background = background.convert('RGBA')
        self.output_image = Image.alpha_composite(background, foreground)

    def get_output_image(self, otype="Image"):
        if otype == "Image":
            return self.output_image
        elif otype == "Base64":
            return base64.b64encode(self.get_output_image(otype="String"))
        elif otype == "String":
            img_io = StringIO()
            self.output_image.save(img_io, 'PNG')
            img_io.seek(0)
            return img_io.getvalue()
