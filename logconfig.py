"""Configure basic logging before any other loggers get set up."""
import logging
import sys

loglevel = logging.getLogger('gunicorn.error').level or logging.DEBUG
fmt = '%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s'
logging.basicConfig(level=loglevel, stream=sys.stdout, format=fmt)
