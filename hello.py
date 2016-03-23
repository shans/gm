from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import json

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class StorePage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        user = users.get_current_user();
        if not user:
            self.response.write('ERROR')
            return
        parent = ndb.Key("User", user.user_id())
        nrc = NameRaceClass.fromJSON(json.loads(self.request.body), parent)
        if not nrc:
            self.response.write('ERROR')
            return
        nrc.put()
        self.response.write('OK')

class RetrieveList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/json'
        user = users.get_current_user();
        if not user:
            self.response.write("[]");
            return
        parent = ndb.Key("User", user.user_id())
        results = NameRaceClass.list(parent);
        response = []
        for result in results:
            response.append({'name': result.key.id(), 'subrace': result.subrace, 'race': result.race, 'clazz': result.clazz})
        self.response.write(json.dumps(response))

class LoadPage(webapp2.RequestHandler):
    def get(self):
        print "load"

# TODO: use expando?
class NameRaceClass(ndb.Model):
    race = ndb.StringProperty(required=True)
    clazz = ndb.StringProperty(required=True)
    subrace = ndb.StringProperty()

    @staticmethod
    def fromJSON(info, parent):
        result = NameRaceClass(id=info['name'], race=info['race'], clazz=info['clazz'], parent=parent)
        if (info['subrace']):
            result.subrace = info['subrace']
        return result

    @classmethod
    def list(cls, parent_key):
        return cls.query(ancestor=parent_key);

def userKeyedLoadStore(list, name):
    list.append((name + 'Store', StorePage))
    list.append((name + 'Load', LoadPage))
    list.append((name + 'List', RetrieveList))

list = []


userKeyedLoadStore(list, "/NameRaceClass")

app = webapp2.WSGIApplication(list, debug=True)
