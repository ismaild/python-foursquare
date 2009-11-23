"""
foursquare.py - v0.1

A simple python wrapper for the foursquare API.

http://www.foursquare.com
http://api.foursquare.com

Created by Ismail Dhorat @ http://zyelabs.net

"""
import urllib
import simplejson

class foursquare():
    def __init__(self):
        self.base_url = 'http://api.foursquare.com'
        self.api_version = 'v1'
        self.url = self.base_url + '/' + self.api_version + '/'
        self.output = '.json'
    
    def _return_result(self, query_url):
        """
        Internal meathod to return the results
        
        Args: query_url
        
        Returns: JSON/Dictionary of the objects returned by the API
        """
        try:
            result = simplejson.load(urllib.urlopen(query_url))
        except:
            result = {'error': 'Error Loading URL', 'response': 'error' }
        return result
        
    def test(self):
        url = self.url
        """ 
        Test if an API request will succeed
        
        Args: None
        
        Returns: 
            True: Test was succesfull
            or 
            False: The query resulted in an Error 
            
        Usage: 
            f = foursquare()
            t = f.test()
            if t: print "I see dead people!" 
        """
        query_url = self.url + 'test' + self.output
        check = self._return_result(query_url)
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
        
        Usgae:
            f = foursquare()
            f.get_cities           
        """
        query_url = self.url + 'cities' + self.output 
        result = self._return_result(query_url)
        return result
    
    def get_venues(self, lat, lon, search='', limit=''):
        """
        Get venues close by for a given longitude and latitude
        
        args: 
          required: 
            latitude, longitude
          optional:
            limit=
            search=
        
        Returns: Dictionary/JSON of Venues close to Lat, Lon passed
        
        Usage:
            f = foursquare()
            v = f.get_venues(-26.091874,28.057225)
        """
        query_url = self.url + 'venues' + self.output
        params = urllib.urlencode({'geolat': lat, 'geolong': lon, 'q': search, 'l': limit})
        query_url = (query_url + '?%s') % params
        result = self._return_result(query_url)
        return result
        
    def get_tips(self, lat, lon, limit=''):
        """
        Get Tips closeby for a given longitude and lattitude
        
        args: 
          required: 
            latitude, longitude
          optional:
            limit=
        Returns Dictionary/JSON of tips for lat,lon passed`
        """
        query_url = self.url + 'tips' + self.output
        params = urllib.urlencode({'geolat': lat, 'geolong': lon, 'l': limit})
        query_url = (query_url + '?%s') % params
        result = self._return_result(query_url)
        return result

        
    
        
        