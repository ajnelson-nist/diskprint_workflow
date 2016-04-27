
-- This software was developed at the National Institute of Standards
-- and Technology by employees of the Federal Government in the course
-- of their official duties. Pursuant to title 17 Section 105 of the
-- United States Code this software is not subject to copyright
-- protection and is in the public domain. NIST assumes no
-- responsibility whatsoever for its use by other parties, and makes
-- no guarantees, expressed or implied, about its quality,
-- reliability, or any other characteristic.
--
-- We would appreciate acknowledgement if the software is used.

PRAGMA foreign_keys = ON;

CREATE TABLE hive_analysis (
    hive_id INTEGER PRIMARY KEY,
    filename TEXT,
    mtime_header TEXT
);

CREATE TABLE cell_analysis (
    cell_id INTEGER PRIMARY KEY,
    hive_id INTEGER,
    parent_cell_id INTEGER,
    cellname TEXT,
    name_type TEXT,
    type TEXT,
    mtime TEXT,
    basename TEXT,

    FOREIGN KEY(hive_id) REFERENCES hive_analysis(hive_id)
);
