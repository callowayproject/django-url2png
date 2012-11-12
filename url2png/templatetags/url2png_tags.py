from django import template
from django.template.defaultfilters import stringfilter

from url2png.settings import THUMBNAIL_MAX_WIDTH, VIEWPORT
from url2png.api import make_api_url, calc_height

register = template.Library()


@register.filter
@stringfilter
def url2png(url, width=THUMBNAIL_MAX_WIDTH):
    """
    Generate the url2png screenshot for a given url.
        {# Use a custom thumbnail width #}
        {{ post.url|url2png:300 }}

        {# Use the configured THUMBNAIL_MAX_WIDTH #}
        {{ post.url|url2png }}
    """
    return make_api_url(url, thumbnail_max_width=width)
url2png.is_safe = True


@register.simple_tag
def get_height(width=THUMBNAIL_MAX_WIDTH, viewport=VIEWPORT):
    """
    Return the height based on the viewport and thumbnail width
    """
    return calc_height(int(width), viewport)

"""
from django.template import Context, Template
t = Template('{% load url2png_tags %}<img src="{{ url|url2png:400 }}" width="300" height="{% get_height 400 %}"/>')
c = Context({'url': 'education.nationalgeographic.com'})
t.render(c)
"""
