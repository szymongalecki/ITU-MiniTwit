#!/bin/bash
TIMEOUT=300  # Timeout in seconds
INTERVAL=5   # Interval in seconds
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
 if /minitwit/check_containers.sh; then
  break
 fi

 ELAPSED=$((ELAPSED + INTERVAL))
 sleep $INTERVAL
done

if [ $ELAPSED -ge $TIMEOUT ]; then
 echo "Service availability check timed out."
 exit 1
fi