# run.py
# Author: Miikka Varri
# Date: February 13, 2016
# Purpose: To get an apartment in Stockholm

import sre, urllib2, sys, BaseHTTPServer, datetime, smtplib, mandrill
from pymongo import MongoClient

# Define url to fetch
listing="http://www.blocket.se/bostad/uthyres/stockholm?sort=&ss=&se=&ros=&roe=&bs=&be=&mre=&q=&q=&q=&is=1&save_search=1&l=0&md=th&f=p&f=c&f=b"
mandril_key="YOUR_MANDRIL_API_KEY"
mailfromemail="sender@domain.com"
mailfrom="Sender name"
mailto="your.email@domain.com"
mongocon="mongodb://localhost"

# Request webpage to receive source
def retrieveWebPage(address):
    try:
    	web_handle = urllib2.urlopen(address)
    except urllib2.HTTPError, e:
    	error_desc = BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
        print "Cannot retrieve URL: HTTP Error Code", e.code
        sys.exit(1)
    except urllib2.URLError, e:
        print "Cannot retrieve URL: " + e.reason[1]
        sys.exit(1)
    except:
        print "Cannot retrieve URL: unknown error"
        sys.exit(1)
    return web_handle

# Store ad url to db
def storeAd(url):
	# Check that url doesent exist
	record = db.find({"url" : url})
	if(record.count() == 0):
		now = datetime.datetime.utcnow()
		db.insert({'url': url, 
			'stored': now, 
			'contacted': False, 
			'alerted': False})

# Send an alert to yourself
def alert(url):
	status = False
	try:
		mandrill_client = mandrill.Mandrill(mandril_key)
		message={
	     'auto_html': None,
	     'auto_text': None,
	     'from_email': mailfromemail,
	     'from_name': mailfrom,
	     'important': False,
	     'subject': 'New apartment ad',
	     'text': 'New ad: '+url,
	     'to': [{'email': mailto,
	             'type': 'to'}]
	     }
		result = mandrill_client.messages.send(message=message, 
			async=False, 
			ip_pool='Main Pool')
		status = True
	except mandrill.Error, e:
		print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    
	return status

match_set = set()

# Get listing html source
website_handle = retrieveWebPage(listing)
website_text = website_handle.read()

# Find matches from listing page.
matches = sre.findall('class="item_link xiti_ad_heading" .*href="(.*?)"', 
	website_text)

# Add matches to match_set
for match in matches:
	match_set.add(match)

match_set = list(match_set)

# Estabilish db connection
connection = MongoClient(mongocon)

# Use ads database and blocket collection
db = connection.ads.blocket

# Iterate urls
for item in match_set:
	storeAd(item)

# find all ads
results = db.find({'alerted': False})

# iterate non alerted ads from collection
for record in results:
	if(alert(record['url'])):
		# If alert was succesfully send mark it as alerted.
		db.update_one({ 'url': record['url']},
			{ '$set': {'alerted': True}})

# close the connection to MongoDB
connection.close()