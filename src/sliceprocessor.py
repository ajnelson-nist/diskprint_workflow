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
This script:
 * Reads the config file, optionally passed with a command-line flag.
 * Connects to the Postgres database.
 * Passes each sequence ID (label) to stdout.
"""

__version__ = "0.4.1"

import os
import sys
import argparse
import logging
import subprocess

_logger = logging.getLogger(os.path.basename(__file__))

import differ_library

def main():
    global args
    _logger.debug("Running main() of file: %r." % __file__)

    (inconn,incursor) = differ_library.db_conn_from_config_path(args.config)

    #Fetch work queue
    query = """
SELECT DISTINCT
  sequencelabel
FROM
  diskprint.namedsequence
ORDER BY
  sequencelabel
;"""
    incursor.execute(query)
    _logger.info("Diskprint table Query: %s" % query)
    inrows = [row for row in incursor]

    for inrow in inrows:
        print(inrow["sequencelabel"])

    if len(inrows) == 0:
        _logger.info("No diskprints to process.")

    #Cleanup
    inconn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Configuration file", default="differ.cfg")
    parser.add_argument("-d", "--debug", help="Enable debug printing", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
      format='%(asctime)s %(levelname)s: %(message)s',
      datefmt='%Y-%m-%dT%H:%M:%SZ',
      level=logging.DEBUG if args.debug else logging.INFO
    )

    main()
