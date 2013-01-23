# -*- coding:utf-8 -*-

import os
import sys
import unicodedata

from google.appengine.ext import db

def slugify(text):
   s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
   return re.sub('[^a-zA-Z0-9-]+', '-', s.lower()).strip('-')

class TGLpost(db.Model):
   path = db.StringProperty(required=True)
   title = db.StringProperty(required=True, indexed=False)
   summary = db.TextProperty(required=True)
   tags = db.ListProperty(StringProperty, indexed=False)
   pubdate = db.DateTimeProperty(required=True)

   @property
   def tag_pairs(self):
      return [(x, utils.slugify(x.lower())) for x in self.tags]
