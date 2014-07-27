import webapp2
import json
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from model.case import Case
from model.step import Step

cpt_codes = set(['CPT-1', 'CPT-2', 'CPT-3', 'CPT-4', 'CPT-5', 'CPT-6', 'CPT-7', 'CPT-8'])

class CaseValueObj():
    def __init__(self):
        self.case = None
        self.case_id = None

class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url('/'))
        else:
            index_path = os.path.join(os.path.dirname(__file__), '../templates/index.html')
            template_params = {'signout_url':users.create_logout_url('/'),
                               'user_name':user.nickname()}
            self.response.out.write(template.render(index_path, template_params))

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
            response['case_id'] = case.key().id()
        self.response.out.write(json.dumps(response))

class NewStepHandler(webapp2.RequestHandler):
    def get(self):
        index_path = os.path.join(os.path.dirname(__file__), '../templates/new_step.html')
        self.response.out.write(template.render(index_path, {'case_id':self.request.get('case_id')}))

class SaveStepHandler(webapp2.RequestHandler):
    def post(self):
        case_id = long(self.request.get('case_id'))
        response = {}
        case = Case.get_by_id(case_id)
        if not case:
            response['error'] = 'Sorry, invalid case ID provided!'
        else:
            step = Step()
            step.case = case
            step.start_time = self.request.get('start_time')
            step.end_time = self.request.get('stop_time')
            step.description = self.request.get('description')
            step.notes = self.request.get('notes')
            step.put()
            response['case_id'] = case.key().id()
        print response
        self.response.out.write(json.dumps(response))

class LibraryHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        email = user.email()
        cases = Case.all()
        cases.filter("user_email =", email)
        cases_val_objs = []
        for curr_case in cases.run(limit=100):
            value_obj = CaseValueObj()
            value_obj.case = curr_case
            value_obj.case_id = curr_case.key().id()
            cases_val_objs.append(value_obj)
        index_path = os.path.join(os.path.dirname(__file__), '../templates/library.html')
        template_params = {'user_name':user.nickname(),
                           'cases':cases_val_objs}
        self.response.out.write(template.render(index_path, template_params))

class SearchCaseHandler(webapp2.RequestHandler):
    def get(self):
        index_path = os.path.join(os.path.dirname(__file__), '../templates/search_case.html')
        self.response.out.write(template.render(index_path, {'cpt_codes':cpt_codes}))

    def post(self):
        cases = Case.all()
        cases.filter("cpt =", self.request.get('cpt'))
        cases_val_objs = []
        for case in cases.run(limit=100):
            value_obj = CaseValueObj()
            value_obj.case = case
            value_obj.case_id = case.key().id()
            cases_val_objs.append(value_obj)
        index_path = os.path.join(os.path.dirname(__file__), '../templates/search_results.html')
        template_params = {'cases':cases_val_objs}
        self.response.out.write(template.render(index_path, template_params))


app = webapp2.WSGIApplication([('/', HomepageHandler),
                               ('/new_case', NewCaseHandler),
                               ('/save_case', SaveCaseHandler),
                               ('/search_case', SearchCaseHandler),
                               ('/new_step', NewStepHandler),
                               ('/save_step', SaveStepHandler),
                               ('/library', LibraryHandler)])
