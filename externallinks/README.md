External Links
==============
This analysis of links on wikipedia looks at external links and language links.
It attempts to find various attributes of the links structure.

Counts
------
Counts of the external links database, based on link semantics (protocol,
domain levels, etc).

The output is stored in `data-externallinks.json` as a multi-level python dictionary:

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

Attributes
----------
Attributes of the external links database, such as most popular sites,
buckets for sites and domains, etc.  Many of the attributes are simply
taken from the Counts dataset rather than doing a full traversal of the db.

    {
      'popular': {
        'protocols': [top 20% of protocols]
        'tlds': [top 10% of tlds]
        'sites': [top .01% of sites]
      }
    }

Requirements
------------
**Data** (see main README for more info on these)

 * enwiki-externallinks db 
