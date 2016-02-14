# Getting an apartment in Stockholm

Finding an apartment in Stockholm is pain in the ass. Highest number of ads could be found from Blocket.se, but their "notify me when new ad is published" functionality is not fast enought. After few weeks you probably get tired of hitting browser refresh button and would like to automate process as much as possible.

## Overview

This Python script checks if specific Blocket.se url contains any new ads and notifies you via email. To make sure emails will arrive instatly, there's Mandril SMTP integration.

Btw, 2000 free email sendouts are givien to you when you create an account to Mandrilapp.com.

All ads are being stored to MongoDB.

## Setting up

Easist way to get started is to set up 24/7 environment and run run.py file every minute with Crobtab.

If you have "home server", Vagrant env could be way to go. I'm using smallest DigialOcean virtual server for this.

You need to set up following variables:

```
// Full url to lising page with possbile filters, get it from your browser.
listing="http://www.blocket.se/bostad/uthyres/stockholm?sort=&ss=&se=&ros=&roe=&bs=&be=&mre=&q=&q=&q=&is=1&save_search=1&l=0&md=th&f=p&f=c&f=b"
mandril_key="YOUR_MANDRIL_API_KEY" // MANDRIL API KEY
mailfromemail="sender@domain.com" // SENDING DOMAIN
mailfrom="Sender name" // SENDING NAME
mailto="your.email@domain.com" // YOUR EMAIL
mongocon="mongodb://localhost" // MONGO DB settings
```

## Next?

Before using this script, you should know that you'll receive a lot of emails (which is good).

Next step will be integrating automated application posting to landlord.