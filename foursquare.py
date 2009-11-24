import urllib2
import urllib
import base64
import simplejson

class foursquare():
    """
    foursquare.py - v0.1.

    A simple python wrapper for the foursquare API.

    http://www.foursquare.com
    http://api.foursquare.com

    Created by Ismail Dhorat @ http://zyelabs.net
    
    Usage:
    foursquare.method(requiredargs, optionalargs)
    
    foursquare.get_cities()    
    foursquare.get_venues(-27.091874,29.057225)
    foursquare.get_venues(-27.091874,29.057225, l=10)
    
    * Optional args are keyword arguments and the keyword is mapped to the get param needed by the foursquare api
    """
    def __init__(self):
        self.url = 'http://api.foursquare.com/v1/'
        self.output = '.json'
    
    def _return_result(self, endpoint, username=None, password=None, params=None):
        """
        Internal method to return the results
        
        Args (required): 
        - endpoint 
        
        keyword args(optional):
        - username
        - password
        - params
        """
        query_url = self.url + endpoint + self.output
        if params:
            query_url = (query_url + '?%s') % urllib.urlencode(params)
        request = urllib2.Request(query_url)

        if username and password:
            b64 = base64.encodestring('%s:%s' % (username, password))[:-1]
            authheader="Basic %s" % b64
            request.add_header('Authorization', authheader)
        return simplejson.load(urllib2.urlopen(request))
        
    def test(self):
        """ 
        Test if an API request will succeed
        
        Args: None
        
        Returns: 
        True -- Test was succesful or
        False -- The query resulted in an Error 
        """
        check = self._return_result('test')
        if check['response'] == 'ok':
            result = True
        else: 
            result = False
        return result
        
    def get_cities(self):
        """
        Returns all cities
        
        Args: None
        """
        return self._return_result('cities')
    
    def get_venues(self, lat, lon, **kwargs):
        """
        Returns venues within range for a given lat & lon
        
        args: 
        latitude -- Required
        longitude -- Required
        
        keyword args (Optional):
        l=10 --- Limit results
        q=food --- search for keyword
        """
        kwargs['geolat'] = lat
        kwargs['geolong'] = lon
        return self._return_result('venues', params=kwargs)
        
    def get_tips(self, lat, lon, **kwargs):
        """
        Returns tips within range of a given lat & lon
        
        args (required): 
        - latitude
        - longitude
        
        Keyword Args (optional):
        - l=10
        """
        kwargs['geolat'] = lat
        kwargs['geolong'] = lon
        return self._return_result('tips', params=kwargs)
    
    def check_city(self, lat, lon):
        """
        Returns the closest foursquare city for a give lat & lon
        
        args (required):
        - lat
        - lon
        """
        params = {'geolat': lat, 'geolong': lon}
        return self._return_result('checkcity', params=params)
    
    def get_venue_detail(self, vid , username=None, password=None,):
        """
        Returns detailed info for a specific venue
        
        args (required):
        - vid 
        
        keyword args (optional):
        - username
        - password
        """
        params = {'vid': vid }
        return self._return_result('venue', username=username, password=password, params=params)
    
    def get_history(self, username, password):
        """
        Returns a history for the authenticated user
        
        args (required):
        - username
        - password
        """
        return self._return_result('history', username=username, password=password)
    
    def get_user_detail(self, username, password, **kwargs):
        """
        Returns user details for a given uid or authenticated user
        
        args (Required):
        - username 
        - password
        
        Keyword Arguments (optional):
        - uid=xxx 
        - mayor=1
        - bages=1
        """
        return self._return_result('user', username=username, password=password, params=kwargs)
    
    def get_friends(self, username, password, **kwargs):
        """
        Returns friends for a given uid or authenticated user
        
        Args (required):
        - username
        - password
        
        keyword args (optional):
        - uid=12345
        """
        return self._return_result('friends', username=username, password=password, params=kwargs)
    
    def get_checkins(self, username, password, **kwargs):
        """
        Returns checkins for friends of authenticated user
        
        Args (required):
        - username
        - password
        
        keyword args (optional):
        - cityid=12345
        """
        return self._return_result('checkins', username=username, password=password, params=kwargs)