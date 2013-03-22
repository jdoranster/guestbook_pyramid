from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import jinja2
import os

from google.appengine.api import users

from models import Greeting, guestbook_key

   
@view_config(route_name='root_view', renderer='mytemplate.jinja2', request_method='GET')
def root_view(request):
     return {'project':'Guestbook on pyramid_appengine'}
        

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

@view_config(route_name='guestbook', renderer='json', request_method='POST')    
def post_guest_view(request):
    greeting = Greeting(parent=guestbook_key())

    if users.get_current_user():
        greeting.author = users.get_current_user()

    greeting.content = request.params['content']
    greeting.put()
    user = 'An anonymous person'
    if users.get_current_user():
        user = users.get_current_user().nickname()
    return {'greeting': greeting.content, 'user': user}

    
