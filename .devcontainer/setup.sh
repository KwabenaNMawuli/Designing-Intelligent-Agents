#!/bin/bash
sudo apt-get update

sudo apt-get install -y prosody lua-sec lua-dbi-sqlite3

pip install --upgrade pip 
pip install spade aioxmpp

echo "Setup complete! SPADE and XMPP server installed"