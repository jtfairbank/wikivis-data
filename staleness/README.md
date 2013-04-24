Staleness of Pages
==================
This analysis of the enwiki pages provides an overview of how stale enwiki is
by counting the number of pages placed in week long buckets based on their last
edit date.

It also provides related analysis:

 * most recently edited page
 * least recently edited page
 * average staleness (X weeks ago)

The output is stored in `data-stateless-namespaced.json` as a multi-level python dictionary:

    {
        'all': {
            'YYYYMM': X1
            ...more months X2, X3, etc...
            'total': X = SUM(Xi)
        },
        'ns': {
            'YYYYMM': X1
            ...more months X2, X3, etc...
            'total': X = SUM(Xi)
        },
        ...more namespaces etc...
    }

Requirements
------------
**Data** (see main README for more info on these)

 * enwiki-page db 
