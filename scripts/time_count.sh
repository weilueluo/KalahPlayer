#!/bin/bash
# Counts the total runtime for a particular bot from a results file.
# Usage: First create the results file
# OneVAll.sh <botname> > <filename>
# time_count <botname> <filename>

### Warning ###
### It does not work in this script. But the command line version does work.
grep "^Player.*$1" $2 | grep -P -o "\b\d{3,}\b" |awk '{sum+=$1;} END {print sum;}' "$@"

