@echo off
pylint %1 | sed "s/^\([A-Z]\):/%~dpnx1:\1:/"