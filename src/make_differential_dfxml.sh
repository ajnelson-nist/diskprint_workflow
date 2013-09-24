#!/bin/bash

#One-liner c/o http://stackoverflow.com/a/246128/1207160
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

dwf_output_dir="$2"
source "$script_dir/_results_sequences.sh"

if [ $dwf_tarball_results_dirs_index_previous -eq -1 ]; then
  echo "Note: Skipping generating difference.  No image comes prior to the beginning of the sequence." >&2
  exit 0
fi

set -e
set -x

baseline="${dwf_tarball_results_dirs[0]}/make_fiwalk_dfxml_alloc.sh/fiout.dfxml"
prior="${dwf_tarball_results_dirs[$dwf_tarball_results_dirs_index_previous]}/make_fiwalk_dfxml_alloc.sh/fiout.dfxml"
current="${dwf_tarball_results_dirs[$dwf_tarball_results_dirs_index_current]}/make_fiwalk_dfxml_alloc.sh/fiout.dfxml"

pushd "${dwf_output_dir}" >/dev/null
/opt/local/bin/python3.3 "$script_dir/idifference.py" --xml from_baseline.xml "$baseline" "$current"
/opt/local/bin/python3.3 "$script_dir/idifference.py" --xml from_prior.xml "$prior" "$current"
status=$?
popd >/dev/null
exit $status
