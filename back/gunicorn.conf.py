import os

#bind = "0.0.0.0:8080"
workers = int(os.environ.get('GUNICORN_WORKERS', 2))
#user = 'www-data'
#group = 'www-data'
