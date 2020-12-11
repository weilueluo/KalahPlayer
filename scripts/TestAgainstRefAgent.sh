#!/bin/bash
# Run agent A against RefAgent both ways
java -jar ManKalah.jar "$1" "/usr/bin/java -jar MKRefAgent.jar"
java -jar ManKalah.jar "/usr/bin/java -jar MKRefAgent.jar" "$1"
