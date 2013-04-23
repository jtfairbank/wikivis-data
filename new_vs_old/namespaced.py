import sys
import os
import MySQLdb as mdb
import json

# hack to import parent package files while using this as a script in a subpackage
sys.path.append(sys.path.append('/'.join(os.getcwd().split('/')[:-1])))
from settings import *

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
            "SELECT page_namespace, page_is_new, count(*) FROM\
                (SELECT page_namespace, page_is_new FROM page LIMIT %s, %s)\
                AS subquery\
            GROUP BY page_namespace, page_is_new",
            (i * LEN, LEN)
        )

        rows = cur.fetchall()

        for row in rows:
            ns = str(row['page_namespace'])
            new = str(row['page_is_new'])
            count = row['count(*)']

            # update namespaced values
            if ns not in results:
                results[ns] = {'total': 0}
            result = results[ns]

            if new not in result:
                result[new] = 0
            result[new] += count

            result['total'] += count

            # update all value
            result = results['all']

            if new not in result:
                result[new] = 0
            result[new] += count

            result['total'] += count

            # update our count of rows
            numRows = result['total']

        i += 1

    # format output and write it
    for ns in results:
        result = results[ns]
        if '0' in result:
            result['old'] = result.pop('0')
        if '1' in result:
            result['new'] = result.pop('1')

    with open('data-new_vs_old-namespaced.json', 'w') as outfile:
        json.dump(results, outfile)

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()
