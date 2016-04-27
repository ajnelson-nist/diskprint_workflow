#!/usr/bin/env python3

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

"""
This program prints a single path to a requested node data component.  For instance, pass 'disk 123-4-567-8-90' to get the path to the disk image file of node_id 123-4-etc.
"""

__version__ = "0.1.2"

import logging
import os

_logger = logging.getLogger(os.path.basename(__file__))

import differ_db_library
import differ_func_library

def main():
    global args
    (conn, cursor) = differ_db_library.db_conn_from_config_path(args.config)

    (osetid, appetid, sliceid) = differ_func_library.split_node_id(args.node_id)

    sql_fetch = """
SELECT
  location
FROM
  diskprint.storage
WHERE
  filetype = %s AND
  osetid = %s AND
  appetid = %s AND
  sliceid = %s
"""
    cursor.execute(sql_fetch, (args.component, osetid, appetid, sliceid))
    rows = [row for row in cursor]

    if len(rows) != 1:
        _logger.debug("osetid = %r." % osetid)
        _logger.debug("appetid = %r." % appetid)
        _logger.debug("sliceid = %r." % sliceid)
        _logger.debug("component = %r." % args.component)
        raise ValueError("Retrieved %d rows from database; expecting at most 1." % len(rows))

    for row in rows:
        print(row["location"])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Configuration file", default="differ.cfg")
    parser.add_argument("--debug", help="Turn on debug-level logging.", action="store_true")
    parser.add_argument("component", help="One of 'disk', 'ram', 'pcap'.")
    parser.add_argument("node_id", help="osetid-appetid-sliceid.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    main()
