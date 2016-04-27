
# For changes made after April 1, 2016:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

__version__ = "0.4.0"

import os
import sys
if sys.version_info < (3,0):
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser
import psycopg2
import psycopg2.extras

import logging
_logger = logging.getLogger(os.path.basename(__file__))

def db_conn_from_config_path(cfg_path):
    """
    Return (Postgres connection, cursor) as a pair.
    """
    config = ConfigParser()
    config.optionxform = str #Without this, config options are case insensitive and the parser pukes on ".exe=something" and ".EXE=somethingelse"
    config.read(cfg_path)                                                                                          
    configrootdict = dict()                                                                                           
    for (n,v) in config.items("root"):                                                                                
        configrootdict[n]=v
    pwfilepath = configrootdict.get("DBpasswordfile")
    if not os.path.isfile(pwfilepath):
        raise Exception("Unable to find database password file: %r." % pwfilepath)
    configrootdict["DBpassword"] = open(pwfilepath, "r").read().strip()                                           
    
    conn_string = "host='%(DBserverIP)s' dbname='%(DBname)s' user='%(DBusername)s' password='%(DBpassword)s'" % configrootdict
    #_logger.debug("conn_string: \"%s\"." % conn_string)
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True                                                                                            
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return (conn, cursor)

def get_sequence_id_from_label(cursor, sequencelabel):
    """This function gets the numeric sequence identifier for a sequence label.  If one does not exist in the database, None is returned."""
    cursor.execute("SELECT sequenceid FROM diskprint.namedsequenceid WHERE sequencelabel = %s;", (sequencelabel,))
    rows = [row for row in cursor]
    if len(rows) == 0:
        return None
    elif len(rows) > 1:
        raise Exception("Uniqueness of sequencelabel violated; multiple entries exist for sequence label %r.  Please inspect." % sequencelabel)
    return rows[0]["sequenceid"]

def make_sequence_id_for_label(conn, cursor, sequencelabel):
    """
    This function gets the numeric sequence identifier for a sequence label.  If one does not exist in the database, one is created in the database and returned.

    (Hence, this function has a potential side-effect in the database, but is idempotent.)
    """
    retval = get_sequence_id_from_label(cursor, sequencelabel)
    if not retval is None:
        _logger.debug("Sequence ID found.")
        return retval
    _logger.debug("Inserting label %r into namedsequenceid..." % sequencelabel)
    cursor.execute("INSERT INTO diskprint.namedsequenceid(sequencelabel) VALUES (%s);", (sequencelabel,))
    _logger.debug("Done inserting.  Committing...")
    conn.commit()
    _logger.debug("Done committing.")
    retval = get_sequence_id_from_label(cursor, sequencelabel)
    if retval is None:
        raise Exception("Database could not retrieve label that should have just been inserted, %r.  Please inspect." % sequencelabel)
    return retval

#This 'main' logic is just for checking that the database is reachable with a given config file
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Configuration file", default="differ.cfg")
    parser.add_argument("--check", help="Check for database connectivity and exit", action="store_true")
    parser.add_argument("--debug", help="Enable debug printing", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
      format='%(asctime)s %(levelname)s: %(message)s',
      datefmt='%Y-%m-%dT%H:%M:%SZ',
      level=logging.DEBUG if args.debug else logging.INFO
    )

    if args.check:
        (conn,cursor) = db_conn_from_config_path(args.config)

        cursor.execute("SELECT COUNT(*) AS tally FROM diskprint.slice;")
        inrows = [row for row in cursor]
        _logger.debug("The slice table currently has %r entries." % inrows[0]["tally"])

        cursor.execute("SELECT COUNT(*) AS tally FROM diskprint.regdelta;")
        inrows = [row for row in cursor]
        _logger.debug("The regdelta table currently has %r entries." % inrows[0]["tally"])

        cursor.execute("SELECT * FROM diskprint.storage;")
        inrows = [row for row in cursor]
        import collections
        nonexists = []
        for row in inrows:
            if not os.path.exists(row["location"]):
                nonexists.append(row["location"])
        _logger.debug("There are %d tarballs in the database that aren't found in the file system." % len(nonexists))
        if len(nonexists) > 0:
            _logger.debug("They are:")
            for path in nonexists:
                _logger.debug("\t%s" % path)
