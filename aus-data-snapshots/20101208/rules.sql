# 3.6.13 build3 available on beta channel, release still on 3.6.12 release version
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.13-build3', 100, 'minor', 'Firefox', '3.6*', 'betatest');
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.13-build3', 100, 'minor', 'Firefox', '3.6*', 'beta');
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.13-build3', 100, 'minor', 'Firefox', '3.6*', 'releasetest');
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '3.6*', 'release');

# how do I write 3.6.11 build1 & 2 -> build3 compactly ?
# that problem goes away with AUS3 due to the many -> latest mapping
INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, buildTarget, buildID, comment) VALUES (50, 'Firefox-3.6.11-build3', 100, 'minor', 'Firefox', '3.6.11', 'Darwin_Universal-gcc3', '20100930123656','Firefox-3.6.11-build1 mac');

# testing NULL matching
#INSERT INTO update_paths (priority, mapping, throttle, update_type, product, version, channel) VALUES (30, 'BigBitBucket', 10, 'major', 'Firefox', NULL, 'release');