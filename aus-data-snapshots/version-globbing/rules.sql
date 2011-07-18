# Globbing at the start
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '*.8', 'release');
# Globbing in the middle
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '3.*.7', 'release');
# Globbing at the end
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '3.6.1*', 'release');
