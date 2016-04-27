#!/usr/bin/env python3

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

__version__ = "0.2.0"

import logging
import os
import sqlite3

_logger = logging.getLogger(os.path.basename(__file__))

def main():
    conn = sqlite3.connect(args.out_db)
    conn.row_factory = sqlite3.Row
    rcursor = conn.cursor()
    wcursor = conn.cursor()

    wcursor.execute("PRAGMA foreign_keys = ON;")

    rcursor.execute("ATTACH DATABASE '%s' AS rx;" % args.rx_db)

    wcursor.execute("""\
INSERT INTO hive_analysis (hive_id, filename, mtime_header)
  SELECT
    hive_id,
    hive_file_path,
    mtime_hive_root
  FROM
    rx.hive_analysis
  ORDER BY
    hive_file_path
;""")

    cell_rowids = dict() #Key: (hive_id, full_path).  Value: rowid.
    rcursor.execute("""\
SELECT
  ca.rowid,
  ca.hive_id,
  ca.full_path,
  ca.cell_type,
  ca.type,
  ca.mtime,
  ca.name
FROM
  rx.cell_analysis AS ca,
  rx.hive_analysis AS ha
WHERE
  ca.hive_id = ha.hive_id
ORDER BY
  ha.hive_file_path,
  ca.full_path
;""")
    for row in rcursor:
        if row["type"] == "root":
            parent_cell_id = None
        else:
            parent_full_path = row["full_path"][ : -len(row["name"])-1 ]
            parent_cell_id = cell_rowids.get((row["hive_id"], parent_full_path))

        #Store rowid of this cell path
        if row["cell_type"] == "key":
            cell_rowids[(row["hive_id"], row["full_path"])] = row["rowid"]

        wcursor.execute("INSERT INTO cell_analysis (cell_id, hive_id, parent_cell_id, cellname, name_type, type, mtime, basename) VALUES (?,?,?,?,?,?,?,?);", (
          row["rowid"],
          row["hive_id"],
          parent_cell_id,
          row["full_path"],
          row["cell_type"],
          row["type"],
          row["mtime"],
          row["name"]
        ))

    rcursor.execute("DETACH DATABASE rx;")
    conn.commit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("rx_db")
    parser.add_argument("out_db")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    main()
