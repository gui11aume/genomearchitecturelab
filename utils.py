# -*- coding:utf -8-

import os
import sys

import jinja2

# Import the content of the 'lib' directory.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
import HTMLEditor

# Globals.
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader([TEMPLATE_DIR, CONTENT_DIR]))

def render_template(template_name, template_vals={}):
   template = JINJA_ENV.get_template(template_name)
   return template.render(template_vals)

class HTMLfixer(HTMLEditor.HTMLStreamer):
   """Fixes HTML from The Grand Locus for this site."""
   def handle_starttag(self, tag, attrs):
      HTMLEditor.HTMLStreamer.handle_starttag(self, tag, attrs)
      if tag == 'blockquote':
         self.out.write('<p>')
   def handle_endtag(self, tag):
      if tag == 'blockquote':
         self.flushdata()
         self.out.write('</p>')
      HTMLEditor.HTMLStreamer.handle_endtag(self, tag)

def fix_html(html):
   return HTMLfixer().process(html)
