# SUMMARY:
#  - 4.0rc2 zu gets a null update
#  - 4.0rc2 -> 4.0.1, for all other locales
# Override updates for 'zu' to be NULL
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, buildID, channel, locale) VALUES(1, 100, NULL, 100, 'minor', 'Firefox', '4.0', '20110318052756', 'release', 'zu');
# Update the other locales to 4.0.1
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, buildID, channel) VALUES(1, 50, 'Firefox-4.0.1-build1', 100, 'minor', 'Firefox', '4.0', '20110318052756', 'release');
# Add another, lower data_version, priority rule for good measure
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, buildID, channel) VALUES(1, 30, NULL, 100, 'minor', 'Firefox', '4.0', '20110318052756', 'release');
