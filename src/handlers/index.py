import webapp2
import json
import os

from google.appengine.ext.webapp import template

class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        index_path = os.path.join(os.path.dirname(__file__), '../templates/index.html')
        self.response.out.write(template.render(index_path, None))

app = webapp2.WSGIApplication([('/', HomepageHandler)])
