===============
Getting Started
===============

#. Install it with ``pip``

   .. code-block:: bash

       pip install django-url2png

#. Configure settings: API_KEY, SECRET_KEY

#. Optionally set optional defaults for the filter, especially THUMBNAIL_MAX_WIDTH

#. Use it in a template

   .. code-block:: django

       {% load url2png_tags %}
       <img src="{{ url|url2png:400 }}" width="400" height="{% get_height 400 %}"/>

   This uses the configured ``THUMBNAIL_MAX_WIDTH``, which is set to ``300``

   .. code-block:: django

       {% load url2png_tags %}
       <img src="{{ url|url2png }}" width="300" height="{% get_height %}"/>
