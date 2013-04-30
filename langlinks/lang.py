import sys
import os
import MySQLdb as mdb
import json
import string
import re

# hack to import parent package files while using this as a script in a subpackage
sys.path.append(sys.path.append('/'.join(os.getcwd().split('/')[:-1])))
from settings import *
import tables as tbl

from langInfo import *

# there are 15 million < X < 16 million language links
LEN = 1000000
con = None

total = 0

langs = {
 'total': 0
}
#{
#  'total': X+Y+...
#  'nl': X
#  'en': Y
#  ...
#}

try:
    # setup mysql
    con = mdb.connect(RDS_host, RDS_name, RDS_pass, RDS_defaultDb)
    cur = con.cursor(mdb.cursors.DictCursor)

    # query all entries in page, in increments of LEN
    i = 0
    while total == i * LEN:
        print i

        # TODO: sql
        cur.execute(
            "SELECT page.page_id, page.page_namespace, page.page_title,\
                langlinks.ll_lang, langlinks.ll_title\
            FROM page, langlinks\
            WHERE page.page_id = langlinks.ll_from\
            LIMIT %s, %s",
            (i * LEN, LEN)
        )

        rows = cur.fetchall()

        for row in rows:
            lang = row['ll_lang']

            # langs
            if lang not in langs:
                 langs[lang] = 0
            langs[lang] += 1
            langs['total'] += 1

            total += 1

        i += 1

    # FINAL OUTPUT: format output and write it
    #TODO
    attrs = {
        'langs': langs
    }

    with open('data-langlinks.json', 'w') as outfile:
        json.dump(attrs, outfile)

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()
