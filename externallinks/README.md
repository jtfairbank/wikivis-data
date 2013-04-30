Links
=====
This analysis of links on wikipedia looks at external links and language links.
It attempts to find various attributes of the links structure.

attributes
----------
Attributes of the links tables, such as most popular, least popular, average
number of links per page.

The output is stored in `data-externallinks-attrs.json` as a multi-level python dictionary:

    {
      'total': # of all links
      'invalid': # of all invalid links

      'protocols': {
        'total': # of links considered in this dataset
        'none': # of links w/ no declared protocol
        'http': # of links with the http protocol
        ...
      }

      'tlds': {
        'total': # of links considered in this dataset
        'ip': # of links that point to an ip address
        'none': # of links with no tld
        'com': # of links with the .com tld
        ...
      }

      'sites': {
        'total': # of links considered in this dataset
        'example.com': # of links to example.com and its subdomains
      }

      'subdomains': # of links w/ a subdomain
    }

Requirements
------------
**Data** (see main README for more info on these)

 * enwiki-externallinks db 
