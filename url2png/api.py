import hashlib
import urllib
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
try:
    import Image
except ImportError:
    from PIL import Image

from django.core.files.base import ContentFile

from url2png.settings import (API_KEY, SECRET_KEY, API_URL, DEFAULT_VIEWPORT,
                              DEFAULT_FULLPAGE, DEFAULT_THUMBNAIL_MAX_WIDTH,
                              THUMBNAIL_MAX_WIDTH, VIEWPORT, FULLPAGE)


def non_default_options(url, viewport=DEFAULT_VIEWPORT, fullpage=DEFAULT_FULLPAGE,
                        thumbnail_max_width=DEFAULT_THUMBNAIL_MAX_WIDTH):
    """
    Returns a Query String with only non-default options.
    """
    output = {'url': url}
    if viewport != DEFAULT_VIEWPORT:
        output['viewport'] = viewport
    if fullpage != DEFAULT_FULLPAGE:
        output['fullpage'] = fullpage
    if thumbnail_max_width != DEFAULT_THUMBNAIL_MAX_WIDTH:
        output['thumbnail_max_width'] = thumbnail_max_width
    return urllib.urlencode(output)


def calc_height(thumb_width, viewport):
    """
    Figure out the height based on the viewport/thumbnail_max_width
    """
    width, height = map(int, viewport.split('x'))
    ratio = float(thumb_width) / width
    return int(height * ratio)


def make_api_url(url, viewport=VIEWPORT, fullpage=FULLPAGE,
                 thumbnail_max_width=THUMBNAIL_MAX_WIDTH):
    options = non_default_options(url, viewport, fullpage, thumbnail_max_width)
    token = hashlib.md5('?%s%s' % (options, SECRET_KEY)).hexdigest()
    result = '/'.join((API_URL, API_KEY, token, 'png/?%s' % options))

    return result


def download_website_image(url, filepath=None, viewport=VIEWPORT,
                           fullpage=FULLPAGE,
                           thumbnail_max_width=THUMBNAIL_MAX_WIDTH):
    """
    Given the url of a webpage, download the thumbnail of the website.

    If filepath is given, image is downloaded into that path, otherwise image
    is saved into a temporary file.

    Returns the filepath to the saved image
    """
    api_params = {
        'url': url,
        'viewport': viewport,
        'fullpage': fullpage,
        'thumbnail_max_width': thumbnail_max_width,
    }
    info = urllib.urlretrieve(make_api_url(**api_params), filepath)
    return info[0]


def django_website_image(url, viewport=VIEWPORT, fullpage=FULLPAGE,
                         thumbnail_max_width=THUMBNAIL_MAX_WIDTH):
    """
    Returns a filename, (width, height), ContentFile tuple for saving in a field

    the filename is a hash of the parameters passed to the function to avoid
    naming collisions

    filename, dimensions, contentfile = django_website_image(self.url)
    self.key_image.save(filename, contentfile)
    """
    api_params = {
        'url': url,
        'viewport': viewport,
        'fullpage': fullpage,
        'thumbnail_max_width': thumbnail_max_width,
    }
    filename = "%s.png" % hashlib.md5(''.join(map(str, api_params.values()))).hexdigest()
    filepath = download_website_image(**api_params)
    image = Image.open(filepath)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    destination = StringIO()
    image.save(destination, format='PNG')
    destination.seek(0)

    return (filename, image.size, ContentFile(destination.read()))
