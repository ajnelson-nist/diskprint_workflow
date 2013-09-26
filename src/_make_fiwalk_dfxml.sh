#!/bin/bash

#This script is not meant to be called directly; it should be sourced.
#The variable maybe_alloc_only might be defined by the including script.

if [ -z "$maybe_alloc_only" ]; then
  echo "The variable \$maybe_alloc_only wasn't found; it should be defined just before including this file." >&2
  exit 1
fi

output_dir="${2}"
path_to_e01="$output_dir/../invoke_vmdk_to_E01.sh/out.E01"
path_to_dfxml="${output_dir}/fiout.dfxml"

fiwalk -G0 "$maybe_alloc_only" -X"$path_to_dfxml" -f "$path_to_e01"

#Just for the DiskPrints project, check that at least one partition was extracted.
if [ $(grep '<volume ' "$path_to_dfxml" | wc -l) -eq 0 ]; then
  echo "Warning: Fiwalk could not extract any partitions from the disk image. This should not be true for Disk Print data (except for the beginning images of the OS series)." >&2
fi