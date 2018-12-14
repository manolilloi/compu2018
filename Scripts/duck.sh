#!/bin/bash
current=""
while true; do
	latest=`ec2metadata --public-ipv4`
	echo "public-ipv4=$latest"
	if [ "$current" == "$latest" ]
	then
		echo "ip not changed"
	else
		echo "ip has changed - updating"
		current=$latest
		echo url="https://www.duckdns.org/update?domains=computacionmemolaunmonton&token=b92e9ebd-4d11-46a2-bca2-31940ca562b4" | curl -k -o ~/duckdns/duck.log -K -
	fi
	sleep 5m
done