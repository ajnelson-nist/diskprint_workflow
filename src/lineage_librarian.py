#!/usr/bin/env python

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
Produces a sequence list for the given sequence-identifying triplet.
"""

__version__ = "0.3.3"

import os
import sys
import logging

import differ_db_library

def list_ids(conn, cursor):
    sql_get_ids = """\
SELECT DISTINCT
  sequencelabel
FROM
  diskprint.namedsequence
ORDER BY
  sequencelabel
;"""
    cursor.execute(sql_get_ids)
    rows = [row for row in cursor]
    for row in rows:
        print(row["sequencelabel"])

def list_nodes(conn, cursor, sequencelabel):
    sql_get_nodes = """\
SELECT
  *
FROM
  diskprint.namedsequence
WHERE
  sequencelabel = %s
ORDER BY
  sliceid
;"""
    cursor.execute(sql_get_nodes, (sequencelabel,))
    rows = [row for row in cursor]
    #AJN TODO This will need a better node's-data mechanism.  For now, though, we're just analyzing disks.
    for (row_no, row) in enumerate(rows):
        #For the first row, print the baseline node if there is one.
        if row_no == 0 and not row["predecessor_osetid"] is None:
            print("%(predecessor_osetid)s-%(predecessor_appetid)s-%(predecessor_sliceid)s" % row)
        print("%(osetid)s-%(appetid)s-%(sliceid)s" % row)

def main():
    global args

    (conn, cursor) = differ_db_library.db_conn_from_config_path(args.config)

    if args.command == "list_ids":
        list_ids(conn, cursor)
    elif args.command == "list_nodes":
        list_nodes(conn, cursor, args.graph_id)

if __name__ == "__main__":
    import argparse

    script_path = os.path.abspath(sys.argv[0])

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Configuration file", default=script_path + ".cfg")
    parser.add_argument("--debug", help="Turn on debug-level logging.", action="store_true")
    parser.add_argument("command", help="One of 'list_ids', 'list_nodes'.")
    #Check args so far to see if we need another.
    (known_args, others) = parser.parse_known_args()

    loglvl = logging.DEBUG if known_args.debug else logging.INFO

    if not known_args.command in ["list_ids", "list_nodes"]:
        raise ValueError("The command must be one of 'list_ids' or 'list_nodes'.  Received %r." % known_args.command)
    elif known_args.command == "list_nodes":
        parser.add_argument("graph_id", help="Graph identifier string.")

    args = parser.parse_args()

    logging.basicConfig(
      format='%(asctime)s %(levelname)s: %(message)s',
      datefmt='%Y-%m-%dT%H:%M:%SZ',
      level=loglvl
    )

    main()
