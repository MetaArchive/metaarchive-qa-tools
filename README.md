# MetaArchive QA Tools

Scripts to help with validating the quality of files in a collection before 
being preserved.

## find-bad-files.py

This tool will recursively scan a directory for filenames that violate a set
of naming standards meant to prevent problems when ingesting collections into
LOCKSS over HTTP.  The relative paths will be printed to standard output; No
files are moved or modified by this tool.

If -v or --verbose is provided, the reasons for the results being matched will
be printed with the output.

### Usage

    find-bad-files.py [-h|--help] [-v|--verbose] <directory>

### Rules enforced

* Characters must be URL-safe. For our purposes, we strictly limit the 
  characters present in filenames to letters, numbers, dots (.), hyphens (-),
  and underscores (_).
* Filenames must start with a letter or number. This prevents inclusion of 
  various hidden files, config files, .DS_store, tilde-prefixed backups, and 
  other likely-undesired files.
* Filenames must not equal "Thumbs.db".

## License

See LICENSE.txt
