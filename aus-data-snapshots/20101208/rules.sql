# 3.6.13 build3 available on beta channel, release still on 3.6.12 release version
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.13-build3', 100, 'minor', 'Firefox', '3.6*', 'betatest');
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.13-build3', 100, 'minor', 'Firefox', '3.6*', 'beta');
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.13-build3', 100, 'minor', 'Firefox', '3.6*', 'releasetest');
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '3.6*', 'release');
# testing NULL matching
#INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (30, 'BigBitBucket', 10, 'major', 'Firefox', NULL, 'release');