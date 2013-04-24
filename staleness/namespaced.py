import sys
import os
import MySQLdb as mdb
import json

# hack to import parent package files while using this as a script in a subpackage
sys.path.append(sys.path.append('/'.join(os.getcwd().split('/')[:-1])))
from settings import *
import tables as tbl

# pages table has 29 mil < X < 30 mil entries
LEN = 1000000

con = None

numRows = 0
results = {
    'all': {
        'total': 0
    }
}

try:
    # setup mysql
    con = mdb.connect(RDS_host, RDS_name, RDS_pass, RDS_defaultDb)
    cur = con.cursor(mdb.cursors.DictCursor)

    # query all entries in page, in increments of LEN
    i = 0
    while numRows == i * LEN:
        print i

        cur.execute(
            "SELECT page_namespace, page_touched_day, count(*) FROM\
                (SELECT\
                    page_namespace,\
                    (page_touched DIV 1000000) as page_touched_day\
                FROM page LIMIT %s, %s)\
                AS subquery\
            GROUP BY page_namespace, page_touched_day",
            (i * LEN, LEN)
        )

        rows = cur.fetchall()

        for row in rows:
            ns = str(row['page_namespace'])
            day = str(row['page_touched_day'])
            month = str(row['page_touched_day']/100)
            count = row['count(*)']

            # update namespaced values
            if ns not in results:
                results[ns] = {'total': 0}
            result = results[ns]

            if month not in result:
                result[month] = 0
            result[month] += count

            result['total'] += count

            # update all value
            result = results['all']

            if month not in result:
                result[month] = 0
            result[month] += count

            result['total'] += count

            # update our count of rows
            numRows += count

        i += 1

    # format output and write it
    tbl.giveMeaning(results, tbl.Page.namespace_map)

    with open('data-staleness-namespaced.json', 'w') as outfile:
        json.dump(results, outfile)

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()
