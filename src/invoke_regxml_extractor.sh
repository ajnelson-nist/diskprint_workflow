#!/bin/bash

path_to_e01="${2/%invoke_regxml_extractor.sh/link_disk.sh}/disk0.E01"
output_dir="${2}"

previous_fiout="${output_dir/%invoke_regxml_extractor.sh/make_fiwalk_dfxml_alloc.sh}/fiout.dfxml"

pushd "${output_dir}"
regxml_extractor.sh -d -x "$previous_fiout" "${path_to_e01}"
status=$?
popd
exit $status
