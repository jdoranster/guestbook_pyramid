from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name='default_guestbook'):
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    
        

@view_config(route_name='guestbook', renderer='guestbook.jinja2', request_method='GET')    
def get_guest_view(request):
    greetings_query = Greeting.query(ancestor=guestbook_key()).order(-Greeting.date)
    greetings = greetings_query.fetch(10)

    if users.get_current_user():
        url = users.create_logout_url(request.url)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(request.url)
        url_linktext = 'Login'

    return {'url_linktext':url_linktext, 'url': url, 'greetings':greetings}

@view_config(route_name='guestbook', renderer='guestbook.jinja2', request_method='POST')    
def post_guest_view(request):
    greeting = Greeting(parent=guestbook_key())

    if users.get_current_user():
        greeting.author = users.get_current_user()

    greeting.content = request.params['content']
    greeting.put()
    return HTTPFound(location='/guestbook')

    
