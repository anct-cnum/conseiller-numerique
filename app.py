import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'back'))
print(sys.path)

from djapp.wsgi import application
