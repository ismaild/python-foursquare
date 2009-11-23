import urllib
import simplejson

class foursquare():
    """
    foursquare.py - v0.1

    A simple python wrapper for the foursquare API.

    http://www.foursquare.com
    http://api.foursquare.com

    Created by Ismail Dhorat @ http://zyelabs.net
    
    Usage:
    foursquare.method(requiredargs, optionalargs)
    
    foursquare.get_cities()    
    foursquare.get_venues(-27.091874,29.057225)
    foursquare.get_venues(-27.091874,29.057225, limit=10)

    """
    def __init__(self):
        self.base_url = 'http://api.foursquare.com'
        self.api_version = 'v1'
        self.url = self.base_url + '/' + self.api_version + '/'
        self.output = '.json'
        self.endpoints = {
            'test': 'test', 
            'cities': 'cities',
            'venues': 'venues',
            'tips' : 'tips'
        }
    
    def _return_result(self, endpoint, params=None):
        """
        Internal method to return the results
        
        Args: 
        endpoint -- required (What kind of request is this?)
        params -- optional (a dictionary of get params and values)
        
        Returns: JSON/Dictionary of the objects returned by the API
        """
        try:
            endpoint = self.endpoints[endpoint]
            query_url = self.url + endpoint + self.output
            if params:
                query_url = (query_url + '?%s') % urllib.urlencode(params)
            try:
                result = simplejson.load(urllib.urlopen(query_url))
            except:
                result = {'error': 'Error Loading URL', 'response': 'error' }
        except:
            result = {'error': 'Invalid Endpoint', 'response':'error'}
        return result
        
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
        Get a list of cities
        
        Args: None
        
        Returns: Dictionary/JSON of All cities   
        """
        return self._return_result('cities')
    
    def get_venues(self, lat, lon, search='', limit=''):
        """
        Get venues close by for a given longitude and latitude
        
        args: 
        latitude -- Required
        longitude -- Required
        
        keyword arguments:
        limit -- Limit the number of records returned
        search -- search for a specific keyword
        
        Returns: Dictionary/JSON of Venues close to Lat, Lon passed
        
        """
        params = {'geolat': lat, 'geolong': lon, 'q': search, 'l': limit}
        return self._return_result('venues', params=params)
        
    def get_tips(self, lat, lon, limit=''):
        """
        Get Tips closeby for a given longitude and latitude
        
        args: 
        latitude -- Required
        longitude -- Required
        
        keyword arguments:
        limit -- Limit the number of records returned
        
        Returns: Dictionary/JSON of tips for lat,lon passed
        """
        params = {'geolat': lat, 'geolong': lon, 'l': limit}
        return self._return_result('tips', params=params)