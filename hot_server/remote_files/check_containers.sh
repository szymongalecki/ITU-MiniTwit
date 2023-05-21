#!/bin/bash
container_count=$(docker ps --format '{{.ID}}' | wc -l)
threshold=10
if [ "$container_count" -lt "$threshold" ]; then
    exit 1  # Return non-zero exit status to trigger switch
else
    exit 0  # Return zero exit status to indicate everything is fine
fi
