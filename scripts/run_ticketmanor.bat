@echo off
rm -rf TicketManor.egg-info
python setup.py develop
@echo on
pserve development.ini --reload