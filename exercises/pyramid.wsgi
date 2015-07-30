from pyramid.paster import get_app, setup_logging
ini_path = 'C:/crs1906/exercises/ticketmanor_venv/ticketmanor_webapp/production.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
