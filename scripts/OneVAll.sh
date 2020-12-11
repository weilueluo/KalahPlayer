#!/bin/bash
# A tournament one against all
# Usage ./OneVAll.sh "agent"

# One goes first
java -jar ManKalah.jar "$1" "java -jar Group1.jar"
java -jar ManKalah.jar "$1" "python3.6 handler.py"
java -jar ManKalah.jar "$1" "java -jar Agent3.jar"
java -jar ManKalah.jar "$1" "java -jar BotGroup4.jar"
java -jar ManKalah.jar "$1" "java -jar 006AgentGroup6.jar"
java -jar ManKalah.jar "$1" "java -jar Group7Agent.jar"
java -jar ManKalah.jar "$1" "python group8_agent.pyxc"
java -jar ManKalah.jar "$1" "java -jar group13.jar"
java -jar ManKalah.jar "$1" "./bot_driver12"
java -jar ManKalah.jar "$1" "java -jar MKAgent14.jar"
java -jar ManKalah.jar "$1" "java -jar MANCalaAgent17.jar"
java -jar ManKalah.jar "$1" "java -jar MKAgent23.jar"
java -jar ManKalah.jar "$1" "java -jar Group24Bot.jar"
java -jar ManKalah.jar "$1" "java -jar Group27Agent.jar"
java -jar ManKalah.jar "$1" "./Group28bot"
java -jar ManKalah.jar "$1" "./kalah_player30"
  
# One goes second
java -jar ManKalah.jar  "java -jar Group1.jar" "$1"
java -jar ManKalah.jar  "python3.6 handler.py" "$1"
java -jar ManKalah.jar  "java -jar Agent3.jar" "$1"
java -jar ManKalah.jar  "java -jar BotGroup4.jar" "$1"
java -jar ManKalah.jar  "java -jar 006AgentGroup6.jar" "$1"
java -jar ManKalah.jar  "java -jar Group7Agent.jar" "$1"
java -jar ManKalah.jar  "python group8_agent.pyxc" "$1"
java -jar ManKalah.jar  "java -jar group13.jar" "$1"
java -jar ManKalah.jar  "./bot_driver12" "$1"
java -jar ManKalah.jar  "java -jar MKAgent14.jar" "$1"
java -jar ManKalah.jar  "java -jar MANCalaAgent17.jar" "$1"
java -jar ManKalah.jar  "java -jar MKAgent23.jar" "$1"
java -jar ManKalah.jar  "java -jar Group24Bot.jar" "$1"
java -jar ManKalah.jar  "java -jar Group27Agent.jar" "$1"
java -jar ManKalah.jar  "./Group28bot" "$1"
java -jar ManKalah.jar  "./kalah_player30" "$1"


