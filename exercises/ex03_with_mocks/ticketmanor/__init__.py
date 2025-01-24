r"""
Creates the Pyramid WSGI application.

To run the app:
    %VENV%\Scripts\pserve development.ini --reload   # restarts server if modules are changed
    Point browser to localhost:6543/html/index.html  # port set in development.ini
To see the Pyramid debug toolbar, replace localhost in the URL with 127.0.0.1
"""
from pyramid.renderers import JSON
from ticketmanor.rest_services.user_service import UserServiceRest

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from pyramid.config import Configurator
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy.orm import sessionmaker
from .models import (
    DBSession,
    Base,
    initialize_sql
)


def db_session(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()

    request.add_finished_callback(cleanup)

    return session


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """

    config = Configurator(settings=settings)
    config.include("pyramid_debugtoolbar")

    # Create the SQLAlchemy DB Engine
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    # Store a session factory in the application's registry, and have
    # the session factory called as a side effect of asking the request
    # object for an attribute. The session object will then have a
    # lifetime matching that of the request.
    # See http://pyramid-cookbook.readthedocs.org/en/latest/database/sqlalchemy.html#using-a-non-global-session
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db_session, reify=True)
    # SQLAlchemy session is now available in view code as
    # request.db_session or config.registry.dbmaker()

    config.include('pyramid_chameleon')

    # Add a view used to render static assets such as images and CSS file.
    # First arg is a URL prefix: ticketmanor:static/theme.css
    # Second arg is path to directory with static resources
    config.add_static_view('static', 'html', cache_max_age=3600)

    # Another option: all URLs in template must be prefixed with ${request.route_url('index')}
    # url_path_prefix = settings['ticketmanor.url_path_prefix']
    url_path_prefix = ""
    add_routes(config, url_path_prefix)

    # Return indented JSON (handy for debugging)
    config.add_renderer('json', JSON(indent=4))

    # The following line allows us to define each model class in its own
    # source file, instead of having to define all model classes in one
    # big file. config.scan() has a side effect of performing a recursive
    # import of the package name it is given. This side effect ensures
    # that each file in ticketmanor.models is imported without requiring
    # that we import each "by hand" within models/__init__.py.
    # See http://pyramid-cookbook.readthedocs.org/en/latest/database/sqlalchemy.html#importing-all-sqlalchemy-models
    config.scan('.models')
    config.scan('.rest_services')
    return config.make_wsgi_app()


def add_routes(config, prefix):
    # config.add_route('index', '/')
    # config.add_route('login_form', '/login_form')
    #    config.add_route('login_form', prefix + '/login_form')
    # config.add_route('login', '/login')
    # config.add_route('add_user_form', '/add_user_form')
    # config.add_route('add_user', '/add_user')

    # http://localhost:6543/rest/news/concerts.json
    config.add_route('get_news', '/rest/news/{news_type}.json')
    config.add_route('get_news_item', '/rest/news/{news_type}/{item_id}.json')
    config.add_route('get_all_news', '/rest/news.json')

    config.add_route('rest_users_email', '/rest/users/{email}')
    config.add_route('rest_users', '/rest/users')

    # config.add_view(UserServiceRest, attr='get_user', request_method='GET')
    # config.add_view(UserServiceRest, attr='add_user', request_method='POST')
    # config.add_view(UserServiceRest, attr='update_user', request_method='PUT')
    # config.add_view(UserServiceRest, attr='delete_user', request_method='DELETE')

    # /rest/events/music.json?event_type=Artist&words=London+Symphony&page=1&page_size=6
    # type: music, sports, movies
    # event_type for music: Artist, Venue, Date, City
    # words: search terms
    config.add_route('rest_events', '/rest/events/{type}.json')
    config.add_route('rest_event', '/rest/events/{type}/{event_id}.json')


# Pyramid mappings of paths to route names
# routes = [
#     ('/', 'index'),
#     ('/login_form', 'login_form'),
#     # (prefix + '/login_form', 'login_form'),
#     ('/login', 'login'),
#     ('/add_user_form', 'add_user_form'),
#     # ('/add_user', 'add_user'),
#     ('/rest/news/{news_type}', 'get_news'),
#     ('/rest/users/{email}', 'rest_users'),  # GET, POST, PUT, DELETE
#     # ('/rest/users/{email}', 'get_user'),  # GET
#     # ('/rest/users', 'add_user'),   # POST
#     # ('/rest/users', 'update_user'),  # PUT
#     # ('/rest/users/delete/{email}', 'delete_user'),  # DELETE
# ]
