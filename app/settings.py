import os

PORT = 8888  # Port for the Tornado application
DEBUG = True  # Enable debugging during development

BASE_LOCATION = os.getcwd()

TEMPLATE_PATH_KEY = 'template_path'
TEMPLATE_PATH = BASE_LOCATION + '\main\src\\templates'

STATIC_URL = '/static/(.*)'
STATIC_PATH = BASE_LOCATION + '\main\src\static'