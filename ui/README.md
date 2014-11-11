# Balrog UI

This is the new Admin UI for [Balrog](https://github.com/mozilla/balrog).
This code might be checked into Balrog proper one day.

# Instructions

To run you first need to install all the npm dependencies:

    npm install

You need [linemanjs](http://linemanjs.com/) to run it:

    npm install -g lineman

To run:

    lineman run

Then open `localhost:8000`.

# Running Tests

To run unit tests, you need to run two terminals. In one:

    lineman run

And in another:

    lineman spec

To run in CI:

    lineman spec-ci

## Test Coverage

Run with [istanbul](https://github.com/yahoo/istanbul) like this:

    istanbul cover generated/js/app.js

You might get an error about (`ReferenceError: window is not defined`)
which is harmless. You can still open the report with:

    open coverage/lcov-report/index.html

## End-to-End Tests

This is not yet developed.
