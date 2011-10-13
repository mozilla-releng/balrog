# The snippets in this test are on release-cck-fallbacktest. Since we're testing
# that they do indeed fallback to release, this is the only rule we need.
INSERT INTO rules (data_version, priority, mapping, throttle, update_type, product, version, channel) VALUES (1, 50, 'Firefox-5.0-build1', 100, 'minor', 'Firefox', '4.0*', 'release');
