#!/bin/bash

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

#Define Pythons
source "${script_dir}/_pick_pythons.sh"

set -e

output_dir="$2"

rx_db="${output_dir}/../invoke_regxml_extractor.sh/out.sqlite"

pushd "${output_dir}" >/dev/null

#Create database
sqlite3 registry_single_state.db < "${script_dir}/registry_single_state_schema.sql"

#Populate database (if input exists and is greater than 0 bytes)
if [ -s "$rx_db" ]; then
  "$PYTHON3" "${script_dir}/format_registry_single_state.py" "$rx_db" registry_single_state.db

  #Verify before and after counts match.
  rx_cell_tally=$(sqlite3 "$rx_db" 'SELECT COUNT(*) FROM cell_analysis;')
  out_cell_tally=$(sqlite3 registry_single_state.db 'SELECT COUNT(*) FROM cell_analysis;')
  if [ $rx_cell_tally -ne $out_cell_tally ]; then
    echo "ERROR:format_registry_single_state.sh:Cell counts before and after re-formatting don't match." >&2
    echo "DEBUG:format_registry_single_state.sh:Before: $rx_cell_tally." >&2
    echo "DEBUG:format_registry_single_state.sh:After: $out_cell_tally." >&2
    exit 1
  fi
fi

popd >/dev/null
