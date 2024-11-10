import os


def log(*args):
    """
    This log function is used to output messages 
    to the console, but only if the ENVIRONMENT variable is set to dev.
    """
    if os.environ.get('ENVIRONMENT') == 'dev':
        print(*args)
 