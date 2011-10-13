# Globbing at the start
INSERT INTO rules (data_version, priority, mapping, throttle, update_type, product, version, channel) VALUES (1, 50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '*.8', 'release');
# Globbing in the middle
INSERT INTO rules (data_version, priority, mapping, throttle, update_type, product, version, channel) VALUES (1, 50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '3.*.7', 'release');
# Globbing at the end
INSERT INTO rules (data_version, priority, mapping, throttle, update_type, product, version, channel) VALUES (1, 50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '3.6.1*', 'release');
