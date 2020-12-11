#!/bin/bash
# Counts the number of wins for a particular bot from a results file.
# Usage: First create the results file
# OneVAll.sh <botname> > <filename>
# winner_count <botname> <filename>
# NOTE: does not count draws. Grep "DRAW" is needed.

grep "WINNER.*$1" $2 |wc -l
