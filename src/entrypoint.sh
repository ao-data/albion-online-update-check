#!/bin/sh
while :
do
	# check for updates
	python albion-online-update-check.py
	
	# sleep for 30 minutes
	sleep 1800
done
