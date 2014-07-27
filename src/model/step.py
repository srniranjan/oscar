from google.appengine.ext import db

class Step(db.Model):
    case = db.ReferenceProperty(indexed=False)
    start_time = db.StringProperty(indexed=False)
    end_time = db.StringProperty(indexed=False)
    description = db.StringProperty(indexed=False)
    notes = db.StringProperty(indexed=False)