from djapp.settings import *

TESTING = True
print('TESTING')

SITE_URL = 'http://testserver.local'

TEST_REQUEST_DEFAULT_FORMAT = 'json'
TEST_REQUEST_RENDERER_CLASSES = [
    'rest_framework.renderers.JSONRenderer',
]