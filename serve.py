# -*- coding: utf-8 -*-

import os
import sys
import gzip
import json
import logging
from StringIO import StringIO

import webapp2
import jinja2

from google.appengine.ext import db
from google.appengine.api import urlfetch

import utils

# Sitemap shit.
class Sitemap(db.Model):
   body = db.BlobProperty()

class SitemapServer(webapp2.RequestHandler):
  def get(self):
     self.response.headers['Content-Type'] = 'application/x-gzip'
     sitemap = Sitemap.get_by_key_name('sitemap')
     self.response.out.write(sitemap.body)

class SitemapRegenerator(webapp2.RequestHandler):
   # Need to manually query "/regenerate_sitemap".
   def get(self):
      content_paths = os.walk('content')
      paths = [
          re.sub('content/', '/', os.path.join(BASE_DIR, file_name))
          for root,dirs,files in content_paths
          for file_name in files
      ]
      sitemap = utils.render_template(
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
      # Ping google.
      google_url = 'http://www.google.com/webmasters/tools/ping?' \
         + 'sitemap=http://lab.thegrandlocus.com/sitemap.xml.gz'
      response = urlfetch.fetch(google_url, '', urlfetch.GET)
      # Does not return, but raise a warning if something goes wrong.
      if response.status_code / 100 != 2:
         logging.warn(
             ("ping failed", response.status_code, response.content)
         )
      else:
         self.response.out.write(response.content)


# Static server shit.
class HardHTMLServer(webapp2.RequestHandler):
   """Server for 'hard' HTML files. Provides only Django templating.
   All hard HTML files have to be in the 'templates' directory."""

   def get(self, path):
      if path == '':
         path = 'index.html'
      if not path.endswith('.html'):
         path += '.html'

      template_vals = {}

      # Fetch last blog post from The Grand Locus.
      if path == 'index.html':
         tglurl = 'http://blog.thegrandlocus.com/lastpost.json'
         response = urlfetch.fetch(tglurl, '', urlfetch.GET)
         if response.status_code / 100 != 2:
            tglpost = None
         else:
            tglpost = json.loads(response.content)
            tglpost['summary'] = utils.fix_html(tglpost['summary'])
         template_vals.update({'tglpost': tglpost})

      try:
         self.response.out.write(utils.render_template(path.lower(),
               template_vals))
      except jinja2.TemplateNotFound:
         self.error(404)
         self.response.out.write(utils.render_template('404.html'))


app = webapp2.WSGIApplication([
  ('/regenerate_sitemap', SitemapRegenerator),
  ('/sitemap.xml.gz', SitemapServer),
  ('/(.*)', HardHTMLServer),
])
