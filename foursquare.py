"""
foursquare.py

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
        
    def test(self):
        url = self.url
        """ 
        Test if an API request will succeed
        
        Args: None
        
        Results: 
            True: Test was succesfull
            or 
            False: The query resulted in an Error 
            
        Usage: 
            f = foursquare()
            t = f.test()
            if t: print "I see dead people!" 
            
        """
        query_url = self.url + 'test' + self.output
        try:
            dump = simplejson.load(urllib.urlopen(query_url))
            if dump['response'] == 'ok':
                result = True
            else: 
                result = False
        except:
            result = False
        return result
        
    def get_cities(self):
        """
        Get a list of cities
        
        Args: None
        
        Results: 
            A dictionary of cities, with lattitude, longitude, name, shortname & id
        
        Usgae:
            f = foursquare()
            f.get_cities
            
        """
        query_url = self.url + 'cities' + self.output 
        try:
            result = simplejson.load(urllib.urlopen(query_url))
        except:
            result = 'There was an error'
        return result


        
    
        
        