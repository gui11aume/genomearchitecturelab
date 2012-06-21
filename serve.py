# -*- coding: utf-8 -*-
import setup_django_version

import os
import re
import gzip
import urllib
from StringIO import StringIO

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.template import _swap_settings
from google.appengine.api import urlfetch

import django.conf
from django import template
from django.template import loader


TEMPLATE_DIRS = ['thegrandlocus_theme/templates', 'content']


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


class Sitemap(db.Model):
   body = db.BlobProperty()


class SitemapServer(webapp.RequestHandler):
  def get(self):
     self.response.headers['Content-Type'] = 'application/x-gzip'
     sitemap = Sitemap.get_by_key_name('sitemap')
     self.response.out.write(sitemap.body)


class SitemapRegenerator(webapp.RequestHandler):
   def get(self):
      content_paths = os.walk('content')
      paths = [
          re.sub('content/', '/', os.path.join(root, file_name)) \
          for root,dirs,files in content_paths \
          for file_name in files
      ]
      sitemap = render_template(
            'sitemap.xml',
            {'paths': paths, 'host': 'lab.thegrandlocus.com'}
      )
      s = StringIO()
      gzip.GzipFile(fileobj=s, mode='wb').write(sitemap)
      s.seek(0)
      Sitemap(
            key_name = 'sitemap',
            body = s.read()
      ).put()
      google_url = 'http://www.google.com/webmasters/tools/ping?' \
         + 'sitemap=http://lab.thegrandlocus.com/sitemap.xml.gz'
      response = urlfetch.fetch(google_url, '', urlfetch.GET)
      # Does not return, but raise a warning if something goes wrong.
      if response.status_code / 100 != 2:
         raise Warning(
             "Google Sitemap ping failed",
             response.status_code,
             response.content
         )
      else:
         self.response.out.write(response.content)




class HardHTMLServer(webapp.RequestHandler):
   """Server for 'hard' HTML files. Provides only Django templating.
   All hard HTML files have to be in the 'templates' directory."""

   def get(self, path):
      path = re.sub('/$', '', path)
      if path == '':
         path = 'index.html'
      self.response.out.write(render_template(path))


application = webapp.WSGIApplication([
  ('/regenerate_sitemap', SitemapRegenerator),
  ('/sitemap.xml.gz', SitemapServer),
  ('/(.*)', HardHTMLServer),
])


def main():
   run_wsgi_app(application)


if __name__ == '__main__':
    main()
