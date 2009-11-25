import urllib2
import urllib
import base64
import simplejson

class Api():
    """
    foursquare.py - v0.1.4

    A simple python wrapper for the foursquare API.

    http://www.foursquare.com
    http://api.foursquare.com

    Created by Ismail Dhorat @ http://zyelabs.net
    
    Usage:
    foursquare.method(requiredargs, optionalargs)
    help(foursquare) -- for help
    
    * Optional args are keyword arguments and the keyword is mapped to the get param needed by the foursquare api
    """
    def __init__(self):
        self.url = 'http://api.foursquare.com/v1/'
        self.output = '.json'
    
    def _return_result(self, endpoint, username=None, password=None, params=None, post=None):
        """
        Internal method to return the results
        
        Args (required): 
        - endpoint 
        
        keyword args(optional):
        - username (Required for authenticated requests)
        - password (required for authenticated requests)
        - params (Optional params)
        - post  (Should be set to True for a http POST request)
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
        True  (Test was succesful)
        False (The query resulted in an Error) 
        """
        check = self._return_result('test')
        return check['response'] == 'ok'
    
    # Geo methods
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
        - geolat  (latitude)
        - geolong  (longitude)
        """
        params = {'geolat': geolat, 'geolong': geolong}
        return self._return_result('checkcity', params=params)
    
    def switch_city(self, username, password, cityid):
        """
        Switch city for authenticated user to a given cityid
        
        args (required):
        - username
        - password
        - cityid
        
        """
        return self._return_result('switchcity', username=username, password=password, params={'cityid': cityid}, post=True)
    
    # Check in methods
    def get_checkins(self, username, password, **kwargs):
        """
        Returns checkins for friends of authenticated user
        
        Args (required):
        - username
        - password
        
        keyword args (optional):
        - cityid
        """
        return self._return_result('checkins', username=username, password=password, params=kwargs)
    
    def checkin(self, username, password, **kwargs):
        """
        Check in the authenticated user
        
        Args (required):
        - username
        - password
        - At least 1 of either vid, shoutout, venue
        
        keyword args (optional)
        - vid  (ID of the venue)
        - venue (String name of the venue)
        - shout (max length is 140)
        - private (1 or 0)
        - twitter (1 or 0, defaults to users setting)
        - geolat
        - geolong
        """
        return self._return_result('checkin', username=username, password=password, params=kwargs, post=True)

    def get_history(self, username, password):
        """
        Returns a history for the authenticated user
        
        args (required):
        - username
        - password
        """
        return self._return_result('history', username=username, password=password)
    
    # User methods
    def get_user_detail(self, username, password, **kwargs):
        """
        Returns user details for a given uid or authenticated user
        
        args (Required):
        - username 
        - password
        
        Keyword Arguments (optional):
        - uid  (userid for the user)
        - mayor (default is false, set to 1 to show)
        - bages (default is false, set to 1 to show)
        """
        return self._return_result('user', username=username, password=password, params=kwargs)
    
    def get_friends(self, username, password, **kwargs):
        """
        Returns friends for a given uid or authenticated user
        
        Args (required):
        - username
        - password
        
        keyword args (optional):
        - uid  (userid for the user)
        """
        return self._return_result('friends', username=username, password=password, params=kwargs)
    
    # Venue methods    
    def get_venues(self, lat, lon, **kwargs):
        """
        Returns venues within range for a given lat & lon
        
        args (required): 
        lat
        lon
        
        keyword args (Optional):
        l   (Limit results)
        q   (search for keyword)
        """
        kwargs['geolat'] = lat
        kwargs['geolong'] = lon
        return self._return_result('venues', params=kwargs)

    def get_venue_detail(self, vid , username=None, password=None,):
        """
        Returns detailed info for a specific venue
        
        args (required):
        - vid 
        
        keyword args (optional):
        - username
        - password
        """
        return self._return_result('venue', username=username, password=password, params={'vid': vid })
    
    def add_venue(self, username, password, name, address, crossstreet, city, state, cityid, **kwargs):
        """
        Adds a new venue
        
        args (required):
        - username
        - password
        - name 
        - address 
        - crossstreet (the cross streets (e.g., "btw Grand & Broome"))
        - city  (city name where this venue is)
        - state  (the state where the city is or for non US insert country for state)
        - cityid  (the cityid for the venue)
        
        Keyword agrs (optional)
        - zip 
        - phone
        """
        params = {'name': name,'address': address,'crossstreet':crossstreet,'city':city,'state':state,'cityid':cityid }
        if kwargs.has_key('phone'):
            params['phone'] = kwargs['phone']
        if kwargs.has_key('zip'):
            params['zip'] = kwargs['zip']
        return self._return_result('addvenue', username=username, password=password, params=params, post=True)
    
    # Tip Methods
        
    def get_tips(self, geolat, geolong, **kwargs):
        """
        Returns tips within range of a given lat & lon
        
        args (required): 
        - geolat
        - geolong
                
        Keyword Args (optional):
        - l (limit results)
        """
        kwargs['geolat'] = geolat
        kwargs['geolong'] = geolong
        return self._return_result('tips', params=kwargs)
    
    def add_tip(self, username, password, vid, text, **kwargs):
        """
        Adds a tip for a specific vid
        
        args (required):
        - username
        - password
        - vid
        - text
        
        keyword args (optional):
        - type ('todo' or 'tip' defaults to tip)
        """
        kwargs['vid'] = vid
        kwargs['text'] = text
        return self._return_result('addtip', username=username, password=password, params=kwargs, post=True)
    
    # Settings Methods 
    def set_pings(self, username, password, **kwargs):
        """
        Change ping settings for authenticated user or for friends of authenticated user
        
        args (required)
        - username
        - password
        - At least one keyword arg
        
        keyword args (optional)
        - me (global ping status for yourself. either on, off or goodnight.)
        - friends (a list of dictionaries, see below)
        
        Note: 
        friends takes a list of dictionaries with the following format: [{'uid': 123, 'ping': 1},{'uid': 123, 'ping': 0}]
         1 = On, 0 = Off
        """
        if kwargs.has_key('me'):
            kwargs['self'] = kwargs['me']
            del kwargs['me']
        if kwargs.has_key('friends'):
            friendlist = kwargs.pop('friends')
            for friend in friendlist:
                kwargs[friend['uid']] = friend['ping']
        return self._return_result('settings/setpings', username=username, password=password, params=kwargs, post=True)