# -*- coding: utf-8 -*-

import os

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Server(webapp.RequestHandler):
   """Minimal server for diagnostic."""
   def get(self):
      self.response.out.write('in development')
      return

application = webapp.WSGIApplication([
  ('/.*', Server),
], debug=True)


def main():
   run_wsgi_app(application)


if __name__ == '__main__':
    main()
