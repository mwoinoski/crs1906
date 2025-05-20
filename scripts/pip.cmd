:: pip 24+ generates deprecation warnings in vendored projects. We have no
:: control over the vendored code, hence those warnings are just noise. So 
:: we'll discard the warnings.

@echo off
powershell -NoProfile -Command "pip3 %* 2>&1 | Where-Object { $_ -notmatch 'DEPRECATION' }"
