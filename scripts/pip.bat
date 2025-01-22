:: pip 24.3.1 generates deprecation warnings in vendored projects. We have no
:: control over the vendored code and the warnings are just noise, so we'll
:: discard the warnings.

@echo off
bash -c "python -m pip %* 2>&1 | grep -v 'DEPRECATION'
