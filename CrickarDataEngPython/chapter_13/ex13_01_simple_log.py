import logging

logging.basicConfig(
    level=0,
    filename='python-log.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info('Something happened')
logging.info('Something else happened, and it was bad')
logging.debug('Attempted to divide by zero')
logging.warning('User left field blank in the form')
logging.error("Couldn't find specified file")
logging.critical('Server is down!')