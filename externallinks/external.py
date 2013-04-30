import sys
import os
import MySQLdb as mdb
import json
import string
from urlparse import urlparse
import re

# hack to import parent package files while using this as a script in a subpackage
sys.path.append(sys.path.append('/'.join(os.getcwd().split('/')[:-1])))
from settings import *
import tables as tbl

from tlds import *

# there are 60 million < X < 61 million external links
LEN = 1000000
con = None

total = 0
invalidCount = 0

protocols = {
    'total': 0,
    'none': 0
}
#{
#    'total': X+Y+Z+...
#    'none': X
#    'http': Y
#    'https': Z
#    ...
#}

tlds = {
    'total': 0,
    'none': 0,
    'ip': 0
}
#{
#    'total': X+Y+Z+...
#    'none': X
#    'com': Y
#    'edu': Z
#    ...
#}

sites = {
    'total': 0,
    'none': 0
}
#{
#    'total': X+Y+Z+...
#    'ip': X
#    'none': Y
#    'example.com': Z
#    ...
#}

subdomainsCount = 0

try:
    # setup mysql
    con = mdb.connect(RDS_host, RDS_name, RDS_pass, RDS_defaultDb)
    cur = con.cursor(mdb.cursors.DictCursor)

    # query all entries in page, in increments of LEN
    i = 0
    while total == i * LEN:
        print i

        cur.execute(
            "SELECT page.page_id, page.page_title, externallinks.el_index\
            FROM externallinks, page\
            WHERE externallinks.el_from = page.page_id\
            LIMIT %s, %s",
            (i * LEN, LEN)
        )

        rows = cur.fetchall()

        for row in rows:
            total += 1

            page_id = str(row['page_id'])
            page_title = str(row['page_title'])
            link = str(row['el_index'])
            # el_index gives a url with the domains reversed:
            #     com.example.www instead of www.example.com

            # parse links and handle invalid cases
            if (link == ""):
                invalidCount += 1
                continue

            url = urlparse(link)
            ip = False # check if domain is an ip address
            if re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.", url[1]):
                ip = True
            domains = string.split(url[1], '.')
            domains = filter(lambda part: part != "", domains)

            if len(domains) == 0:
                #print "No domains: " + link
                invalidCount += 1
                continue

            # protocol
            protocol = url[0]
            if protocol == "":
                #print "No protocol: " + link
                invalidCount += 1
                protocol = "none"
            if protocol not in protocols:
                protocols[protocol] = 0
            protocols[protocol] += 1

            protocols['total'] += 1

            # tlds
            if ip:
                # tld = '.'.join(str(x) for x in domains)
                tlds['ip'] += 1
                tlds['total'] += 1
                continue

            tld = domains[0]
            if (tld not in gtlds) and (tld not in ctlds):
                #print "Unkown tld: " + link
                tld = "[none]"

            if tld == "":
                #print "No tld: " + link
                invalidCount += 1
                tld = "none"

            if tld not in tlds:
                tlds[tld] = 0
            tlds[tld] += 1

            tlds['total'] += 1

            # domains
            if len(domains) > 1:
                domain = domains[1] + "." + domains[0]

                if domain not in sites:
                    sites[domain] = 0
                sites[domain] += 1

            sites['total'] += 1

            # subdomains
            if len(domains) > 2 and not ip:
                subdomainsCount += 0;

        i += 1

        # CHECKPOINT: format output and write it
        attrs = {
            'total': total,
            'invalid': invalidCount,
            'protocols': protocols,
            'tlds': tlds,
            'sites': sites,
            'subdomains': subdomainsCount
        }

        with open('data/data-externallinks-attrs-' + str(i) + '.json', 'w') as outfile:
            json.dump(attrs, outfile)

    # FINAL OUTPUT: format output and write it
    attrs = {
        'total': total,
        'invalid': invalidCount,
        'protocols': protocols,
        'tlds': tlds,
        'sites': sites,
        'subdomains': subdomainsCount
    }

    with open('data-externallinks-attrs.json', 'w') as outfile:
        json.dump(attrs, outfile)

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()
