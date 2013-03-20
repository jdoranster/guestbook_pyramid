from pyramid.config import Configurator
import views
import pyramid_jinja2
import os

__here__ = os.path.dirname(os.path.abspath(__file__))


def make_app():
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator()
    config.add_renderer('.jinja2', pyramid_jinja2.Jinja2Renderer)
    #config.add_view(views.my_view,
    #                renderer='mytemplate.jinja2',
    #                route_name='root')

    config.add_route('guestbook','/guestbook')
    #config.add_view(views.guestbook_view, 
    #                renderer='guestbook.jinja2',
    #                route_name='guestbook')

    config.add_static_view(name='static',
                           path=os.path.join(__here__, 'static'))

    config.scan('unomas')

    return config.make_wsgi_app()

application = make_app()
