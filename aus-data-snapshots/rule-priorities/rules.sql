# SUMMARY:
#  - 4.0rc2 zu gets a null update
#  - 4.0rc2 -> 4.0.1, for all other locales
# Override updates for 'zu' to be NULL
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, buildID, channel, locale) VALUES(100, NULL, 100, 'minor', 'Firefox', '4.0', '20110318052756', 'release', 'zu');
# Update the other locales to 4.0.1
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, buildID, channel) VALUES(50, 'Firefox-4.0.1-build1', 100, 'minor', 'Firefox', '4.0', '20110318052756', 'release');
# Add another, lower priority rule for good measure
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, buildID, channel) VALUES(30, NULL, 100, 'minor', 'Firefox', '4.0', '20110318052756', 'release');
