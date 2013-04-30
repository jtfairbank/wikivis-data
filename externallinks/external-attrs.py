import sys
import os
import MySQLdb as mdb
import json
import string

# hack to import parent package files while using this as a script in a subpackage
sys.path.append(sys.path.append('/'.join(os.getcwd().split('/')[:-1])))
from settings import *
import tables as tbl

from tlds import *

# load in data
counts = json.load( open('data-externallinks.json', 'r') )

protocols = counts['protocols']
pTotal = protocols.pop('total')

tlds = counts['tlds']
tTotal = tlds.pop('total')

sites = counts['sites']
sTotal = sites.pop('total')

# setup output
popular = {}

# find popular
orderedProtocols = map(None, protocols.iteritems())
orderedProtocols.sort(None, lambda item: item[1], True)
orderedProtocols = map(lambda pair: {pair[0]: pair[1]}, orderedProtocols)
popular['protocols'] = orderedProtocols[0:len(orderedProtocols)/5]

orderedTlds = map(None, tlds.iteritems())
orderedTlds.sort(None, lambda item: item[1], True)
orderedTlds = map(lambda pair: {pair[0]: pair[1]}, orderedTlds)
popular['tlds'] = orderedTlds[0:len(orderedTlds)/10]

orderedSites = map(None, sites.iteritems())
orderedSites.sort(None, lambda item: item[1], True)
orderedSites = map(lambda pair: {pair[0]: pair[1]}, orderedSites)
popular['sites'] = orderedSites[0:len(orderedSites)/10000]

# output attrs
attrs = {
    'popular': popular
}

json.dump(attrs, open('data-externallinks-attrs.json', 'w'))
