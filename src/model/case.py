from google.appengine.ext import db

class Case(db.Model):
    cpt = db.StringProperty()
    name = db.StringProperty(indexed=False)
    surgeon_type = db.StringProperty(indexed=False)
    mrn = db.StringProperty(indexed=False)
    dos = db.StringProperty(indexed=False)
    clinical_info = db.StringProperty(indexed=False)