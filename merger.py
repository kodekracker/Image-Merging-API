#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module has a class Merger which takes two urls of images
    and it returns the merged image .And , also contains a utility
    function get_image , return an Image object by downloading a
    image of given url.
"""

import requests
import base64
import os
from os.path import splitext
from os.path import basename
from StringIO import StringIO
from PIL import Image
from requests.exceptions import Timeout
from requests.exceptions import RequestException
from uuid import uuid4
from md5 import md5

__author__ = "Akshay Pratap Singh"
__copyright__ = "Copyright 2014, Ophio Project"
__credits__ = ["Saurabh Kumar"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Akshay Pratap Singh"
__email__ = "pratapakshay0@gmail.com"
__status__ = "Development"


class Error(Exception):
    """
        Exception raised for errors in the module.

        Attributes:
            message -- explanation of the error
    """
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return repr(self.message)


class FormatError(Error):
    """
        Exception raised for errors in invalid image format/url.
    """
    pass


def get_image(url):
    """
        Return Image object after downloading the image via Url

        Parameters:
            url -- an url of png image

        Returns:
             an Image object

        Raises:
            RequestException -- if there is problem in connection
    """
    while True:
        try:
            r = requests.get(url,stream=True)
            im = Image.open(StringIO(r.content))
            return im
        except Timeout:
            continue
        except Exception:
            raise RequestException


def is_image_url(url):
    """
        Returns true if url is in valid form else raises exception
    """
    if url.startswith('http://') or url.startswith('https://'):
        imagename, ext = splitext(basename(url))
        if ext and ext.lower() == ".png":
            return True
    raise FormatError()


class Merger:
    """
        Merge two png images (i.e background and foreground)

        Attributes:
            foreground_url -- url of foreground image
            background_url -- url of background image
            output_image -- Image object contains output image
            output_image_name -- name of output_image

        Methods:
            set_foreground -- sets the foreground_url
            set_background -- sets the background_url
            merge_images -- merge foreground and background images
            get_output_image -- gets the output_image in different types
            save_output_image_to_directory -- save output_image to directory
    """
    def __init__(self, fore_url=None, back_url=None):
        """
            Sets the foreground_url and background_url
        """
        self.foreground_url = fore_url
        self.background_url = back_url
        self.output_image = None
        self.output_image_name = None

    def set_foreground(self,url):
        """
            Sets the foreground_url

            Parameters:
                url -- url of foreground image
        """
        self.foreground_url = url

    def set_background(self,url):
        """
            Sets the background_url

            Parameters:
                url -- url of background image
        """
        self.background_url = url

    def merge_images(self):
        """
            Merge foreground_url and background_url and Sets
            output_image

            Raises:
                Exception -- if any exceptions occur
        """
        try:
            foreground = None
            background = None

            if is_image_url(self.foreground_url):
                foreground = get_image(self.foreground_url)

            if is_image_url(self.background_url):
                background = get_image(self.background_url)

            foreground = foreground.convert('RGBA')
            background = background.convert('RGBA')

            self.output_image = Image.alpha_composite(background, foreground)
            self.save_output_image_to_directory()

        except FormatError:
            raise Error('Not a valid format')
        except RequestException:
            raise Error('Error in Request')
        except Exception:
            raise Error('Some other error')

    def get_output_image(self, otype="Image"):
        """
            Gets the output(i.e merged) image

            Attributes:
                otype -- tells the return type of output_image
        """
        otype = otype.lower()
        if otype == "name":
            return self.output_image_name
        if otype == "image":
            return self.output_image
        elif otype == "base64":
            return base64.b64encode(self.get_output_image(otype="String"))
        elif otype == "string":
            img_io = StringIO()
            self.output_image.save(img_io, 'PNG')
            img_io.seek(0)
            return img_io.getvalue()

    def save_output_image_to_directory(self):
        """
            Saves the output_image to images/ directory
        """
        curr_directory = os.path.dirname(os.path.abspath(__file__))
        path = curr_directory + "/images/"
        if not os.path.exists(path):
            os.makedirs(path)
        self.output_image_name = md5(str(uuid4())).hexdigest()+".jpeg"
        image_file = 'images/'+self.output_image_name
        self.output_image.save(image_file)


if __name__ == '__main__':
    try:
        url1 = 'htp://akshayon.net/images/foreground.png'
        url2 = 'http://akshayon.net/images/background.png'
        m = Merger(url1, url2)
        m.merge_images()
        m.get_output_image(otype="Image").show()
    except Exception as e:
        print 'Error : ', e.message
