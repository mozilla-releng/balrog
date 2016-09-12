# Balrog UI

[![Build Status](https://travis-ci.org/mozilla/balrog-ui.svg?branch=master)](https://travis-ci.org/mozilla/balrog-ui)

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

## End-to-End Tests

This is not yet developed.
