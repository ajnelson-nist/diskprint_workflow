
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
import logging
_logger = logging.getLogger(os.path.basename(__file__))

def split_node_id(node_id_string):
    parts = node_id_string.split("-")
    try:
        assert len(parts) == 5
    except AssertionError as e:
        _logger.error("Unexpected format of node id string: %r" % node_id_string)
        raise
    osetid = "-".join(parts[0:2])
    appetid = "-".join(parts[2:4])
    sliceid = int(parts[4])
    return (osetid, appetid, sliceid)
