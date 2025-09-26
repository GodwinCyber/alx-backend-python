from datetime import datetime
import logging

# Configure logging for this middleware
logger = logging.getLogger('request_logger')
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    '''Class whose instance are cllable'''
    def __init__(self, get_response):
        '''One time configuration and initialization'''
        self.get_response = get_response

    def __call__(self, request):
        '''Code to be executed for each request before
        the view (and later middleware) are called.'''
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logging.info(f'{datetime.now()} - User: {user} - Path: {request.path}')
        response = self.get_response(request)
        return response




