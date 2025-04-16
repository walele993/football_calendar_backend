#!/bin/bash

# Installa tutte le dipendenze
pip install -r requirements.txt

# Raccogli i file statici (senza chiedere conferma)
python manage.py collectstatic --noinput
