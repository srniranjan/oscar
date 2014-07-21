import webapp2
import json
import os

from google.appengine.ext.webapp import template
from model.case import Case

cpt_codes = set(['CPT-1', 'CPT-2', 'CPT-3', 'CPT-4', 'CPT-5', 'CPT-6', 'CPT-7', 'CPT-8'])

class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        index_path = os.path.join(os.path.dirname(__file__), '../templates/index.html')
        self.response.out.write(template.render(index_path, None))

class NewCaseHandler(webapp2.RequestHandler):
    def get(self):
        index_path = os.path.join(os.path.dirname(__file__), '../templates/new_case.html')
        self.response.out.write(template.render(index_path, {'cpt_codes':cpt_codes}))

class SaveCaseHandler(webapp2.RequestHandler):
    def post(self):
        cpt_code = self.request.get('cpt')
        response = {}
        if cpt_code not in cpt_codes:
            response['error'] = 'Sorry, invalid CPT code entered!'
        else:
            case = Case()
            case.cpt = cpt_code
            case.name = self.request.get('name')
            case.surgeon_type = self.request.get('surgeon_type')
            case.mrn = self.request.get('mrn')
            case.clinical_info = self.request.get('clinical_info')
            case.dos = self.request.get('dos')
            case.put()
            response['case-id'] = case.key().id()
        self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([('/', HomepageHandler),
                               ('/new_case', NewCaseHandler),
                               ('/save_case', SaveCaseHandler)])
