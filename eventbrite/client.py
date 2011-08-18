"""Simple Eventbrite client for the HTTP-based API
"""
import datetime
import httplib
import logging
import urllib
from eventbrite import json_lib

EVENTBRITE_DATE_STRING = "%Y-%m-%d %H:%M:%S"
EVENTBRITE_LOGGER = logging.getLogger(__name__)

# Input transformations
def _datetime_to_string(incoming_datetime):
    return incoming_datetime.strftime(EVENTBRITE_DATE_STRING)

def _string_to_datetime(incoming_string):
    return datetime.strptime(incoming_string, EVENTBRITE_DATE_STRING)

def _boolean_one_or_zero(is_true):
    return (is_true and '1') or '0'

def _boolean_true_or_false(is_true):
    return (is_true and 'true') or 'false'

def _comma_separated_list(input_list):
    return ",".join(input_list)

class EventbriteClient(object):
    """Client for Eventbrite's HTTP-based API"""
    eventbrite_api_endpoint = 'www.eventbrite.com'
    eventbrite_request_template = 'https://%(host)s/json/%(method)s?%(arguments)s'
    def __init__(self, app_key=None, user_key=None, password=None):
        """Initialize the client with the given app key and the user key"""
        self._https_connection = httplib.HTTPSConnection(self.eventbrite_api_endpoint)
        self._app_key = app_key
        if password:
            self._username = user_key
            self._password = password
        else:
            self._user_key = user_key

    # dynamic methods handler - call API methods on the local client object
    def __getattr__(self, method):
        def _call(*args, **kwargs):
            return self._request(method, args)
        return _call

    #def _execute_api_call(self, method, params):
    def _request(self, method='', params=dict()):
        """Execute an API call on Eventbrite using their HTTP-based API

        method - string  - the API method to call - see https://www.eventbrite.com/doc
        params - dict    - Arguments to pass along as method request parameters

        Returns: A dictionary with a return structure defined at http://developer.eventbrite.com/doc/
        """
        #unpack our params
        if len(params) > 0: 
            method_arguments = dict(params[0])
        else:
            method_arguments = dict()

        # add the authentication tokens provided during initialization
        if self._app_key:
            method_arguments['app_key'] = self._app_key
        if self._user_key:
            method_arguments['user_key'] = self._user_key
        elif( self._username and self._password):
            method_arguments['user'] = self._username
            method_arguments['password'] = self._password
            
        # urlencode API method parameters
        encoded_params = urllib.urlencode(method_arguments)
        
        # construct our request url
        request_url = self.eventbrite_request_template % dict(host=self.eventbrite_api_endpoint, method=method, arguments=encoded_params)
        EVENTBRITE_LOGGER.debug("REQ - %s", request_url)

        # Send a GET request to Eventbrite
        self._https_connection.request('GET', request_url)

        # Read the JSON response 
        response_data = self._https_connection.getresponse().read()
        EVENTBRITE_LOGGER.debug("RES - %s", response_data)

        # decode our response
        response = json_lib.loads(response_data)
        if 'error' in response and 'error_message' in response['error'] :
            raise EnvironmentError( response['error']['error_message'] )
        return response
