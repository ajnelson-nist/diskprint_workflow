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

git submodule init deps/python-cybox
git submodule sync deps/python-cybox
git submodule update deps/python-cybox

#The rest of this script is a pseudo-git-submodule tracker.  Will be replaced on transitioning to Git.

AFFLIB_REPO=https://github.com/simsong/AFFLIBv3.git
AFFLIB_COMMIT=82511e26b8920334c86a970ea19de3cdc84b4e5e
DFXMLSCHEMA_REPO=https://github.com/ajnelson/dfxml_schema.git
DFXMLSCHEMA_COMMIT=532f994ef652df030cd3f7b96b0870d3fffaec68
DFXML_REPO=https://github.com/simsong/dfxml.git
DFXML_COMMIT=87d51b64f187097906919339cb0d1142d60204f7
RE_REPO=https://github.com/ajnelson-nist/regxml_extractor.git
RE_COMMIT=86d44b00d085201042ad73c85298b4a5b054a3d1

#Fetch Git repositories with git-submodule...only, in SVN.

if [ ! -d deps/regxml_extractor.git ]; then
  echo "Note: Cloning RegXML Extractor Git repository." >&2
  pushd deps/ >/dev/null
  git clone $RE_REPO regxml_extractor.git
  pushd regxml_extractor.git >/dev/null
  git checkout $RE_COMMIT
  popd >/dev/null
  popd >/dev/null
fi

if [ ! -d deps/dfxml_schema.git ]; then
  echo "Note: Cloning DFXML Schema Git repository." >&2
  pushd deps/ >/dev/null
  git clone $DFXMLSCHEMA_REPO dfxml_schema.git
  popd >/dev/null
fi

if [ ! -d deps/dfxml.git ]; then
  echo "Note: Cloning DFXML Git repository." >&2
  pushd deps/ >/dev/null
  git clone $DFXML_REPO dfxml.git
  popd >/dev/null
fi

if [ ! -d deps/AFFLIBv3.git ]; then
  echo "Note: Cloning AFFLib Git repository." >&2
  pushd deps/ >/dev/null
  git clone $AFFLIB_REPO AFFLIBv3.git
  popd >/dev/null
fi
