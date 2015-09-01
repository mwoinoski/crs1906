@rem venv\Scripts\deactivate
@rem virtualenv venv
@rem venv\Scripts\activate
mkdir logs
set EXINIT=set aw
@rem activate.bat:
@rem "PROMPT=$P$+$_$G"
@rem "PROMPT=(ex n.1 venv)"
@call vim setup.py development.ini production.ini ticketmanor\html\javascripts\ticketmanor\views\shared\header.html venv\Scripts\activate.bat
pushd \Users\user\Downloads
pip install coverage-4.0b1-cp34-none-win_amd64.whl
popd
pushd \Users\user\Downloads\mysql-connector-python-2.0.4
python setup.py install
popd
python -m pip install --upgrade pip
pip install -r ..\ticketmanor_webapp\requirements.txt
