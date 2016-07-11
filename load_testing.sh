!# /usr/bin/env bash
# This mimics sending an Ajax to the server
ab -c 50 \
-n 200 \
-H "X-Requested-With: XMLHttpRequest" \
-T "application/x-www-form-urlencoded" \
-p test.data \
-g plot.dat \
-m POST \
http://127.0.0.1:5000/post
