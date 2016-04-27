#!/bin/bash

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

#One-liner c/o http://stackoverflow.com/a/246128/1207160
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
top_srcdir="${script_dir}/.."

source "${top_srcdir}/src/_pick_pythons.sh"

set -e
set -x

for PYTHON in "$PYTHON2" "$PYTHON3"; do
  $PYTHON "${top_srcdir}/src/differ_db_library.py" --config="${top_srcdir}/src/differ.cfg" --check --debug
done

set +x
echo "All's well."
echo "Done."
