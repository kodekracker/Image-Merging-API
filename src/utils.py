"""
    Basic Utility Methods needed
"""


def is_image_url(url):
    """
        Returns true if url is in valid form else false
    """
    if url.startswith('http://') or url.startswith('https://'):
        return True
    return False


DEFAULT_FORMATS = ['PNG']


def is_format_match(image, formats=None):
    """
        Returns true if image format is matched in given formats
        else false
    """
    if not formats:
        formats = DEFAULT_FORMATS
    for f in formats:
        if image.format == f:
            return True
    return False


def cmp_tuples(t1, t2):
    """
        Returns true if two tuples contain same content else false
    """
    return len(t1) == len(t2) and set(t1) == set(t2)


def is_same_size(img1, img2):
    """
        Returns true if both images have same size else false
    """
    img1_size = img1.size
    img2_size = img2.size
    return cmp_tuples(img1_size, img2_size)
