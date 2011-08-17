#eventbrite-client.py#

##Description##
Simple client for Eventbrite's HTTP-based API

Client provides the following:

* Basic type validation of arguments
* Basic checks for required arguments
* Dictionary-based returns as described in Eventbrite's API documentation

For information, see http://developer.eventbrite.com/doc/

##Usage Examples##

###Installation###

NOTE:  This package requires a JSON library - by default we check for "simplejson" or use the built-in "json" library provided in python 2.6+

####Installation using easy_install####

    easy_install eventbrite

####Installation using pip####

    pip install eventbrite

###Loading the Eventbrite API Client###

    import eventbrite

###Initializing the Client###

    # Set your API / Application key - http://eventbrite.com/api/key
    app_key = 'YOUR_APP_KEY'
    # Set your user_key - http://eventbrite.com/userkeyapi
    user_key = 'YOUR_USER_KEY'
    # Initialize the API Client
    eb_client = eventbrite.EventbriteClient(app_key, user_key)

###Calling API methods###

    # try running dir(eb_client) to see the list of available methods
    #   Here is an example for calling the API's user_list_events method
    eb_client.list_user_events()

##Links##
* 0.2x source <http://github.com/mtai/eventbrite/>
