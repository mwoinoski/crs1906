@echo off
call %VIRTUAL_ENV%\Scripts\deactivate
cd %1
venv\Scripts\activate
