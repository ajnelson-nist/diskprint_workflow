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

node_id1="$1"
dwf_output_dir="$2"

#Fetch node_id0
source "${script_dir}/_results_sequences.sh"

pre_db="${dwf_all_results_root}/by_node/${node_id0}/format_registry_single_state.sh/registry_single_state.db"
post_db="${dwf_all_results_root}/by_node/${node_id1}/format_registry_single_state.sh/registry_single_state.db"

pushd "$dwf_output_dir" >/dev/null

#Create database
sqlite3 registry_new_cellnames.db < "${script_dir}/registry_single_state_schema.sql"

#Populate database
"$PYTHON3" "${script_dir}/make_registry_diff_db.py" \
  "$pre_db" \
  "$post_db" \
  registry_new_cellnames.db

popd >/dev/null

