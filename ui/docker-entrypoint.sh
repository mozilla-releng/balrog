#!/bin/bash

cd /app
/usr/local/bin/npm install
# The container we run npm/lineman in uses up a lot of CPU by default, and appears to be
# related to all the polling of files that lineman/grunt does. We haven't been able to
# fully track it down, but jlorenzo discovered that adjusting this setInterval has made a
# huge difference without affecting the responsiveness of the UI rebuilding.
# This really needs a deeper investigation, and a more robust fix.
sed -i -e 's/200/10000/' /app/node_modules/lineman/node_modules/grunt-watch-nospawn/tasks/watch.js
/usr/local/bin/npm build
/usr/local/bin/npm start
