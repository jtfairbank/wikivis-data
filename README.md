wikivis
=======
The wikivis project is an attempt to visualize various aspects of Wikipedia
using their publicly available database dumps and other public data sources.

The project uses Amazon EWS to store the data and perform calculations.

Terms
-----
 * `enwiki` = the English Wikipedia
 * `wiki` = a shorthand for Wikimedia

EWS Setup
---------
The current setup is listed below.  It may not be optimal; I played it safe and
over-allocted resources.

 * 1x db.m2.xlarge RDS instance - 300 Gb
 * 1x m2.2xlarge EC2 instance
 * 1x EBS for EC2 - 100 Gb

**Costs:** TODO

Project Setup
-------------
 1. Clone the project onto the EC2 instance's EBS.
 2. Copy settings.py.skel to settings.py and fill in the values.  This file is
    .gitignore'd so don't worry about accidentally committing your private info.
 3. VirtualEnv: TODO
 4. Pip: TODO


Data Sources
============
The following data sources are used to find meaningful data about Wikipedia:

 * enwiki database dumps: http://dumps.wikimedia.org/enwiki/
 * wiki databases and layout info: http://www.mediawiki.org/wiki/Manual:Database_layout
 * wiki pagecounts: http://dumps.wikimedia.org/other/pagecounts-raw/

Specific information on data sources and EWS loading instructions are listed below.

Loading Data into RDS
---------------------
Since parts of this process take quite a while, I use Pipe Viewer to watch
their progress: http://www.ivarch.com/programs/pv.shtml

 1. Download the data into the EC2 instance:

        curl LINK > FILE

 2. Uncompress the data files (if needed):

        pv COMPRESSED_FILE | gzip -d > DATA_FILE

 3. Use [this guide](http://aws.amazon.com/articles/2933) to import data into RDS.

    Small data files (< 1Gb): don't split- just load the whole file in as one chunk.

    Large data files: split them, then load in each chunk.
    
        pv DATA_FILE | split -l 1000
        pv ALL_CHUNKS | mysql --host=HOST --user=USER --password DB_NAME

enwiki-page db
--------------
Source: http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz

**Loading:** use the standard procedure (above); you can load this db in all at
once (no splitting needed).
