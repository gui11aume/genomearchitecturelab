# -*- coding: utf-8 -*-

import os

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Server(webapp.RequestHandler):
   """Minimal server."""
   def get(self):
      template_vals = {}
      template_path = os.path.join(
          os.path.dirname(__file__),
          'templates',
          'base.html'
      )
      self.response.out.write(template.render(
          template_path,
          template_vals
      ))

application = webapp.WSGIApplication([
  ('/.*', Server),
], debug=True)


def main():
   run_wsgi_app(application)


if __name__ == '__main__':
    main()
