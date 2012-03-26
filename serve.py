# -*- coding: utf-8 -*-
import setup_django_version

import os
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.template import _swap_settings

import django.conf
from django import template
from django.template import loader


TEMPLATE_DIRS = ['content']


def render_template(template_name, template_vals=None):
   """Shameless port of the function of the same name
   by Nick Johnson from Bloggart."""

   old_settings = _swap_settings({'TEMPLATE_DIRS': TEMPLATE_DIRS})
   try:
      tpl = loader.get_template(template_name)
      rendered = tpl.render(template.Context(template_vals))
   finally:
      _swap_settings(old_settings)
   return rendered


class HardHTMLServer(webapp.RequestHandler):
   """Server for 'hard' HTML files. Provides only Django templating.
   All hard HTML files have to be in the 'templates' directory."""

   def get(self, path):
      path = re.sub('/$', '', path)
      if path == '':
         path = 'index.html'
      self.response.out.write(render_template(path))

application = webapp.WSGIApplication([
  ('/(.*)', HardHTMLServer),
])


def main():
   run_wsgi_app(application)


if __name__ == '__main__':
    main()
