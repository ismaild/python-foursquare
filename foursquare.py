import urllib2
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
            'tips' : 'tips',
            'checkcity': 'checkcity',
            'switchcity': 'switchcity'
        }
    
    def _return_result(self, endpoint, params=None):
        """
        Internal method to return the results
        
        Args: 
        endpoint -- required (What kind of request is this?)
        params -- optional (a dictionary of get params and values)
        """
        endpoint = self.endpoints[endpoint]
        query_url = self.url + endpoint + self.output
        if params:
            query_url = (query_url + '?%s') % urllib.urlencode(params)
        print query_url
        result = simplejson.load(urllib2.urlopen(query_url))
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
        Returns all cities
        
        Args: None
        """
        return self._return_result('cities')
    
    def get_venues(self, lat, lon, search='', limit=''):
        """
        Returns venues within range for a given lat & lon
        
        args: 
        latitude -- Required
        longitude -- Required
        
        keyword arguments:
        limit -- optional 
        search -- optional
        """
        params = {'geolat': lat, 'geolong': lon, 'q': search, 'l': limit}
        return self._return_result('venues', params=params)
        
    def get_tips(self, lat, lon, limit=''):
        """
        Returns tips within range of a given lat & lon
        
        args: 
        latitude -- Required
        longitude -- Required
        
        keyword arguments:
        limit -- optional
        """
        params = {'geolat': lat, 'geolong': lon, 'l': limit}
        return self._return_result('tips', params=params)
    
    def check_city(self, lat, lon):
        """
        Returns the closest foursquare city for a give lat & lon
        
        args:
        lat - required
        lon - required
        """
        params = {'geolat': lat, 'geolong': lon}
        return self._return_result('checkcity', params=params)