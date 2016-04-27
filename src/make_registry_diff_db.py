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

__version__ = "0.1.3"

import sqlite3
import logging
import os

_logger = logging.getLogger(os.path.basename(__file__))

def main():
    conn = sqlite3.connect(args.out_db)
    conn.row_factory = sqlite3.Row
    rcursor = conn.cursor()
    wcursor = conn.cursor()

    wcursor.execute("PRAGMA foreign_keys = ON;")

    rcursor.execute("ATTACH DATABASE '%s' AS pre;" % args.pre_db)
    rcursor.execute("ATTACH DATABASE '%s' AS post;" % args.post_db)

    wcursor.execute("INSERT INTO main.hive_analysis (hive_id, filename, mtime_header) SELECT hive_id, filename, mtime_header FROM post.hive_analysis ORDER BY filename;")

    #Build translation dictionary of hive IDs that are semantically in-common between the two images.
    pre_to_post_hive_id = dict()
    rcursor.execute("SELECT a.hive_id AS x, b.hive_id AS y FROM pre.hive_analysis AS a, post.hive_analysis AS b WHERE a.filename = b.filename;")
    for row in rcursor:
        pre_to_post_hive_id[row["x"]] = row["y"]

    #Build set of Hive IDs and paths from preimage
    pre_cells = set()
    rcursor.execute("SELECT hive_id, cellname FROM pre.cell_analysis;")
    for row in rcursor:
        post_hive_id = pre_to_post_hive_id.get(row["hive_id"])
        if post_hive_id is None:
            #If the hive's absent in the postimage, there won't be any new cells in it.  Skip tracking this.
            continue
        pre_cells.add((post_hive_id, row["cellname"]))

    #Build set of Hive IDs and paths from postimage not in preimage
    post_cells = set()
    rcursor.execute("SELECT * FROM post.cell_analysis ORDER BY hive_id, cellname;")
    for row in rcursor:
        if (row["hive_id"], row["cellname"]) in pre_cells:
            continue
        wcursor.execute("INSERT INTO main.cell_analysis (cell_id, hive_id, parent_cell_id, cellname, name_type, type, mtime, basename) VALUES (?,?,?,?,?,?,?,?);", (
          row["cell_id"],
          row["hive_id"],
          row["parent_cell_id"],
          row["cellname"],
          row["name_type"],
          row["type"],
          row["mtime"],
          row["basename"]
        ))

    rcursor.execute("DETACH DATABASE post;")
    rcursor.execute("DETACH DATABASE pre;")
    conn.commit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("pre_db")
    parser.add_argument("post_db")
    parser.add_argument("out_db")
    args = parser.parse_args()
    main()
