#!/bin/sh
set -e

# Start Nginx in background
nginx -g "daemon off;" &

# Wait for a few seconds to let Nginx start
sleep 5

# Test the configuration
nginx -T

# Wait for Nginx process to finish
wait
