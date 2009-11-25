""""

Foursquare.py - v0.1.1
=======================
A simple python wrapper for the foursquare API.

http://www.foursquare.com
http://api.foursquare.com

Created by Ismail Dhorat @ http://zyelabs.net

License: see the file 'License'

Usage:
foursquare.method(requiredargs, optionalargs)
help(foursquare) - for help

Notes:
- arguments are required.
- keyword arguments are optional.
- the keyword is mapped to the key required by the foursquare API (except for set_pings).
- if authentication is required, username and password are the first two args.

"""

import urllib2
import urllib
import base64

try:
    import simplejson
except:
    print 'Please install the required module simplejson'

class Api():
    """
        Foursquare API class that implements methods for the API
    
        args: None 
    """
    def __init__(self):
        self.url = 'http://api.foursquare.com/v1/'
        self.output = '.json'
    
    def _return_result(self, endpoint, username=None, password=None, params=None, post=None):
        """
            Internal method to return the results
        
            Arguments (Required):
                ``endpoint``
                    The foursquare API endpoint for this request
        
            Keyword Arguments (Optional):
                ``username``
                    Required for authenticated requests
                ``password``
                    required for authenticated requests
                ``params``
                    Optional GET/POST parameters to send to the foursquare API
                ``post``
                    Only required for HTTP POST requests, set to True
        """
        
        query_url = self.url + endpoint + self.output
        if not post:
            if params:
                data = urllib.urlencode(params)
                request = urllib2.Request('%s?%s' % (query_url, data) )
            else:
                request = urllib2.Request(query_url)
        else:
            if params:
                data = urllib.urlencode(params)
                request = urllib2.Request(query_url, data)
            else:
                request = urllib2.Request(query_url)

        if username and password:
            b64 = base64.encodestring('%s:%s' % (username, password))[:-1]
            authheader="Basic %s" % b64
            request.add_header('Authorization', authheader)
        try:
            result = simplejson.load(urllib2.urlopen(request))
        except IOError, e:
            if e.code:
                result = e
        return result
        
    def test(self):
        """ 
            Test if an API request will succeed
        
            Args: None
        
            Returns: 
                ``True``
                    Test was succesful
                ``False``
                    The query resulted in an Error
        """
        check = self._return_result('test')
        return check['response'] == 'ok'
    
    def get_cities(self):
        """
            Returns all cities
        
            Args: None
        """
        return self._return_result('cities')

    def check_city(self, geolat, geolong):
        """
            Returns the closest foursquare city for a give lat & lon
        
            args (required):
        
            ``geolat``
                latitude
            ``geolong``
                longitude
        """
        params = {'geolat': geolat, 'geolong': geolong}
        return self._return_result('checkcity', params=params)
    
    def switch_city(self, username, password, cityid):
        """
            Switch city for authenticated user to a given cityid
        
            args (required):
        
            ``username``
                username of the user
            ``password``
                password of the user
            ``cityid``
                the foursquare cityid being switched to
        """
        return self._return_result('switchcity', username=username, password=password, params={'cityid': cityid}, post=True)
    
    def get_checkins(self, username, password, **kwargs):
        """
            Returns checkins for friends of authenticated user
        
            args (required):
                ``username``
                    username of the user
                ``password``
                    password of the user
        
            keyword args (optional):
                ``cityid``
                    the foursquare cityid
        """
        return self._return_result('checkins', username=username, password=password, params=kwargs)
    
    def checkin(self, username, password, **kwargs):
        """
            Check in the authenticated user
        
            Args (required):
                ``username``
                    username of the user
                ``password``
                    password of the user
                   
            keyword args (optional):
                ``vid``
                    Foursquare venue ID
                ``venue``
                    String name of the venue - The API will try and find the closest match
                ``shout``
                    Text to send with checkin, max length is 140
                ``private`` 
                    hides location set to 1 or 0
                ``twitter``
                    1 or 0, defaults to setting in the users profile
                ``geolat``
                    latitude
                ``geolong``
                    longitude
        """
        if kwargs.has_key('vid') or kwargs.has_key('venue') or kwargs.has_key('shout'):
            result = self._return_result('checkin', username=username, password=password, params=kwargs, post=True)
        else:
            result = 'CheckIn method requires at least one of: vid, venue or shout'
        return result

    def get_history(self, username, password):
        """
        
            Returns a history for the authenticated user
        
            args (required):
            ``username``
                username of the user
            ``password``
               password of the user
        """
        return self._return_result('history', username=username, password=password)
    
    def get_user_detail(self, username, password, **kwargs):
        """
            Returns user details for a given uid or authenticated user
        
            args (Required):
            ``username``
                username of the user
            ``password``
                password of the user
        
            Keyword Arguments (optional):
        
            ``uid``
                userid for the user
            ``mayor``
                default is false, set to 1 to show
            ``bages``
                default is false, set to 1 to show
        
        """
        return self._return_result('user', username=username, password=password, params=kwargs)
    
    def get_friends(self, username, password, **kwargs):
        """
            Returns friends for a given uid or authenticated user
        
            Args (required):
                ``username``
                    username of the user
                ``password``
                    password of the user
        
            keyword args (optional):
                ``uid``
                    userid for the user
        """
        return self._return_result('friends', username=username, password=password, params=kwargs)

    def get_venues(self, geolat, geolong, **kwargs):
        """
            Returns venues within range for a given lat & lon
        
            args (required): 
                ``geolat``
                    latitude
                ``geolong``
                    longitude
        
            keyword args (Optional):
                ``l``
                    Limit the results returned
                ``q``
                    search for a keyword
        """
        kwargs['geolat'] = geolat
        kwargs['geolong'] = geolon
        return self._return_result('venues', params=kwargs)

    def get_venue_detail(self, vid , username=None, password=None,):
        """
            Returns detailed info for a specific venue
        
            args (required):
                ``vid``
                    Foursquare venue ID
        
            keyword args (optional):
                ``username``
                    username of the user
                ``password``
                    password of the user
        """
        return self._return_result('venue', username=username, password=password, params={'vid': vid })
    
    def add_venue(self, username, password, name, address, crossstreet, city, state, cityid, **kwargs):
        """
            Adds a new venue
        
            args (required):
                ``username``
                    username of the user
                ``password``
                    password of the user
                ``name``
                    the venue name
                ``address`` 
                    the address of the venue
                ``crossstreet`` 
                    the cross streets (e.g., "btw Grand & Broome")
                ``city``
                    city name where this venue is)
                ``state``
                    the state where the city is or for non US insert country for state)
                ``cityid``
                    the cityid for the venue
        
        Keyword agrs (optional)
            ``zip``
                zip or postal code
            ``phone``
                phone number of the venue
        
        """
        params = {'name': name,'address': address,'crossstreet':crossstreet,'city':city,'state':state,'cityid':cityid }
        if kwargs.has_key('phone'):
            params['phone'] = kwargs['phone']
        if kwargs.has_key('zip'):
            params['zip'] = kwargs['zip']
        return self._return_result('addvenue', username=username, password=password, params=params, post=True)
        
    def get_tips(self, geolat, geolong, **kwargs):
        """
            Returns tips within range of a given geplat & geolong
        
            args (required): 
                ``geolat``
                    latitude
                ``geolong``
                    longitude
                
            Keyword Args (optional):
                ``l`` 
                    limit results returned
        """
        kwargs['geolat'] = geolat
        kwargs['geolong'] = geolong
        return self._return_result('tips', params=kwargs)
    
    def add_tip(self, username, password, vid, text, **kwargs):
        """
            Adds a tip for a specific vid
        
            args (required):
                ``username``
                    username of the user
                ``password``
                    password of the user
                ``vid``
                    Foursquare venue ID
                ``text``
                    the tip text
            
            keyword args (optional):
                ``type``
                    Set it as 'todo' or 'tip', defaults to tip
        """
        kwargs['vid'] = vid
        kwargs['text'] = text
        return self._return_result('addtip', username=username, password=password, params=kwargs, post=True)
    
    def set_pings(self, username, password, **kwargs):
        """
            Change ping settings for authenticated user or for friends of authenticated user
        
            args (required):
                ``username``
                    username of the user
                ``password``
                    password of the user
        
            keyword args (optional):
                ``me`` 
                    Set global ping status for yourself. options are: on, off or goodnight
                ``friends`` 
                    a list of dictionaries
        
        Note: 
        
        - friends takes a list of dictionaries in the following format: [{'uid': 123, 'ping': 1},{'uid': 123, 'ping': 0}]
        - 1 = On
        - 0 = Off
         
        """
        if kwargs.has_key('me'):
            kwargs['self'] = kwargs['me']
            del kwargs['me']
        if kwargs.has_key('friends'):
            friendlist = kwargs.pop('friends')
            for friend in friendlist:
                kwargs[friend['uid']] = friend['ping']
        return self._return_result('settings/setpings', username=username, password=password, params=kwargs, post=True)