from distutils.core import setup
try:
    import simplejson
except:
    print 'Warning: simplejson module is required'
 
long_description = open('README').read()
 
setup(
    name='foursquare',
    version="0.1.1",
    py_modules = ['foursquare'],
    description='A python library for the foursquare API',
    author='Ismail Dhorat',
    author_email='ismail@zyelabs.net',
    license='BSD License',
    url='http://github.com/zyelabs/python-foursquare/',
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)