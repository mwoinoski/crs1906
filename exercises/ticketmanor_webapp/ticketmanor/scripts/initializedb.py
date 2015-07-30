"""
Script to connect to MySQL and add a record to the database
"""

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    Base,
    DBSession,
)
from ..models.person import Person

usage_msg = """usage: {cmd} config-uri [var=value]
    Example: {cmd} development.ini create_tables=True
    create_tables=True: create and populate DB tables"""


def usage(argv):
    cmd = os.path.basename(argv[0])
    print(usage_msg.format(cmd=cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    print("Running {} with {}".format(os.path.basename(argv[0]), argv[1]))
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    if options.get('create_tables'):
        Base.metadata.create_all(engine)
    with transaction.manager:
        model = Person(
            first_name="John",
            middles="William",
            last_name="Coltrane",
            email="john.coltrane@gmail.com",
            street="342 W 12th St Apt 3C",
            city="New York",
            state="NY",
            country="USA",
            post_code="10012"
        )
        DBSession.add(model)
        print("Added Person '{model.name}'".format(model=model))
        model = Person(
            first_name="Alfred",
            middles="McCoy",
            last_name="Tyner",
            email="mccoy.tyner@gmail.com",
            street="342 W 12th St 3D",
            city="New York",
            state="NY",
            country="USA",
            post_code="10012"
        )
        DBSession.add(model)
        print("Added Person '{model.name}'".format(model=model))
