import webapp2
import json
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from model.case import Case

cpt_codes = set(['CPT-1', 'CPT-2', 'CPT-3', 'CPT-4', 'CPT-5', 'CPT-6', 'CPT-7', 'CPT-8'])

class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url('/'))
        else:
            index_path = os.path.join(os.path.dirname(__file__), '../templates/index.html')
            self.response.out.write(template.render(index_path, {'signout_url':users.create_logout_url('/')}))

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
            user = users.get_current_user()
            case = Case()
            case.user_email = user.email()
            case.cpt = cpt_code
            case.name = self.request.get('name')
            case.surgeon_type = self.request.get('surgeon_type')
            case.mrn = self.request.get('mrn')
            case.clinical_info = self.request.get('clinical_info')
            case.dos = self.request.get('dos')
            case.put()
            response['case-id'] = case.key().id()
        self.response.out.write(json.dumps(response))

class SearchCaseHandler(webapp2.RequestHandler):
    def get(self):
        index_path = os.path.join(os.path.dirname(__file__), '../templates/search_case.html')
        self.response.out.write(template.render(index_path, {'cpt_codes':cpt_codes}))

    def post(self):
        cases = Case.all()
        cases.filter("cpt =", self.request.get('cpt'))
        for case in cases.run(limit=10):
            print case.name
        print cases.cursor()

app = webapp2.WSGIApplication([('/', HomepageHandler),
                               ('/new_case', NewCaseHandler),
                               ('/save_case', SaveCaseHandler),
                               ('/search_case', SearchCaseHandler)])
