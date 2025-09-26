from datetime import datetime, timedelta
import logging
from django.utils.timezone import now
from django.http import HttpResponseForbidden

# configure logging
logger = logging.getLogger('request_logger')
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

resquest_log = {}

class RequestLoggingMiddleware:
    '''Middleware that logs user requests with timestamp, user, and path.'''
    def __init__(self, get_response):
        '''One time configuration and initialization.'''
        self.get_response = get_response

    def __call__(self, request):
        '''Code to be executed for each request before
        the view (and later middleware) are called.'''
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        logger.info(f'{datetime.now()} - User: {user} - Path: {request.path}')
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    ''''Middleware that restricts access to the messaging up during (6pm - 9pm)'''
    def __init__(self, get_response):
        '''One time configuration and initialization'''
        self.get_response = get_response
        self.start_hour = 18 # 6pm
        self.end_hour = 21 # 9pm

    def __call__(self, request):
        '''Executed for every request before the view is called.'''
        current_hour = datetime.now().hour
        if self.start_hour <= current_hour < self.end_hour:
            return HttpResponseForbidden ('Access is restricted, you cannot access this app at this time')
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    '''Middleware that will limit the message a user can send within a window period based on the IP address'''
    def __init__(self, get_response):
        '''One time Congiguration and initializations'''
        self.get_response = get_response
        self.text_limit = 5 # number of text a user can text
        self.time_limit = 60 # time required for a user to send another text is 60mins
        self.user_activity = {}


    def __call__(self, request):
        '''Execute time limit a user can send a text'''
        if request.mthod == 'POST' and 'message' in request.POST:
            user_ip = self.get_user_ip(request)
            now_time = now()

            # initilaize user history is not present
            if user_ip not in self.user_activity:
                self.user_activity[user_ip] = []


            # remove old timestamp outside the time window
            self.user_activity[user_ip] = [
                t for t in self.user_activity[user_ip]
                if now_time - t < timedelta(minutes=self.time_limit)
            ]

            # check limit
            if len(self.user_activity[user_ip]) >= self.text_limit:
                return HttpResponseForbidden('You are blocked for sending further message, Try again later')
            
            # log this message attempt
            self.user_activity[user_ip].append(now_time)
        return self.get_response(request)


    def get_user_ip_address(self, request):
        '''Helper to extract user's IP address from request'''
        x_fowarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_fowarded_for:
            ip = x_fowarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

        