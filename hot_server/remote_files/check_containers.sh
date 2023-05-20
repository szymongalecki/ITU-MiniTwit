#!/bin/bash

# Get the count of running Docker containers
container_count=$(docker ps --format '{{.ID}}' | wc -l)

# Define the threshold for container count
threshold=10

if [ "$container_count" -lt "$threshold" ]; then
    exit 1  # Return non-zero exit status to trigger switch
else
    exit 0  # Return zero exit status to indicate everything is fine
fi
