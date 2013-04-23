New vs. Old Pages
=================
This analysis of the enwiki pages looks at how many are 'new' (have never been
edited) and how many are 'old' (have been edited at least once).  It provides
new, old, and total page counts for each page namespace, as well as an overall
count 'all'.

The output is stored in `data-namespaced.json` as a multi-level python dictionary:

    {
        'all': {
            'new': X = SUM(X1, X2, ...)
            'old': Y = SUM(Y1, Y2, ...)
            'total': X + Y
        },
        '0': {
            'new': X1
            'old': Y1
            'total': X1 + Y1
        },
        ...more namespaces 1, 2, etc...
    }

Requirements
------------
**Data** (see main README for more info on these)

 * enwiki-page db 
