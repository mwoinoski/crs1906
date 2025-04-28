:: pip 24+ generates deprecation warnings in vendored projects. We have no
:: control over the vendored code and the warnings are just noise, so we'll
:: discard the warnings.

@echo off
@echo in pip.cmd
powershell -NoProfile -Command "pip3 %* 2>&1 | Where-Object { $_ -notmatch 'DEPRECATION' }"
