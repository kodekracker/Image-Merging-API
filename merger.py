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
from StringIO import StringIO
from PIL import Image
from requests.exceptions import Timeout
from requests.exceptions import RequestException

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
        Base class for exceptions in this module.
    """
    pass

class InputError(Error):
    """Exception raised for errors in the input.

        Attributes:
            message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class FormatError(Error):
    """Exception raised for errors in the image format.

        Attributes:
            message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


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
            if r.status_code == '200':
                im = Image.open(StringIO(r.content))
                return im
            else:
                raise RequestException
        except Timeout:
            continue
        except RequestException:
            raise RequestException


class Merger:
    """
        Merge two png images (i.e background and foreground)

        Attributes:
            foreground_url -- url of foreground image
            background_url -- url of background image
            output_image -- Image object contains output image
    """
    def __init__(self, fore_url=None, back_url=None):
        """
            Sets the foreground_url and background_url
            and output_image to None
        """
        self.foreground_url = fore_url
        self.background_url = back_url
        self.output_image = None

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
            foreground = get_image(self.foreground_url)
            background = get_image(self.background_url)
            foreground = foreground.convert('RGBA')
            background = background.convert('RGBA')
            self.output_image = Image.alpha_composite(background, foreground)
        except Exception as e:
            raise Exception

    def get_output_image(self, otype="Image"):
        """
            Gets the output(i.e merged) image

            Attributes:
                otype -- tells the return type of output_image
        """
        if otype == "Image":
            return self.output_image
        elif otype == "Base64":
            return base64.b64encode(self.get_output_image(otype="String"))
        elif otype == "String":
            img_io = StringIO()
            self.output_image.save(img_io, 'PNG')
            img_io.seek(0)
            return img_io.getvalue()

if __name__ == '__main__':
    try:
        url1 = 'http://akshayon.net/images/foregrounda.png'
        url2 = 'http://akshayon.net/images/background.png'
        m = Merger(url1, url2)
        m.merge_images()
        decoded_data = base64.b64decode(m.get_output_image(otype="Base64"))
        im = Image.open(StringIO(decoded_data))
        im.show()
    except Exception as e:
        print 'Error occured'
