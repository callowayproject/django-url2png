import hashlib

from url2png.settings import (API_KEY, SECRET_KEY, API_URL, DEFAULT_VIEWPORT,
                              DEFAULT_FULLPAGE, DEFAULT_THUMBNAIL_MAX_WIDTH,
                              THUMBNAIL_MAX_WIDTH, VIEWPORT, FULLPAGE)

def non_default_options(url, viewport=DEFAULT_VIEWPORT, fullpage=DEFAULT_FULLPAGE,
                        thumbnail_max_width=DEFAULT_THUMBNAIL_MAX_WIDTH):
    """
    Returns a Query String with only non-default options.
    """
    import urllib
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
