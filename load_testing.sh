#!/usr/bin/env bash

echo "------------------------Starting Load Testing------------------------"
# The tests mimic sending an Ajax to the server and
#  track the statistics from the server.

ab -c 50 \
-n 200 \
-H "X-Requested-With: XMLHttpRequest" \
-T "application/x-www-form-urlencoded" \
-p test.data \
-g plot.dat \
-m POST \
http://127.0.0.1:5000/post

echo "--------------------------End Load Testing--------------------------"
