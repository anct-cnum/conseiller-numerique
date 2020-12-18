from djapp.settings import *

TESTING = True
print('TESTING')

SITE_URL = 'http://testserver.local'

REST_FRAMEWORK.update({
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
})