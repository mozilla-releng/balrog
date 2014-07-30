# 3.6.13 build3 available on beta channel, release still on 3.6.12 release version
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, channel) VALUES (1, 50, 'Firefox-3.6.13-build3', 100, 'minor', 'Firefox', 'betatest');
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, channel) VALUES (1, 50, 'Firefox-3.6.13-build3', 100, 'minor', 'Firefox', 'beta');
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, channel) VALUES (1, 50, 'Firefox-3.6.13-build3', 100, 'minor', 'Firefox', 'releasetest');
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, channel) VALUES (1, 50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', 'release');

# how do I write 3.6.11 build1 & 2 -> build3 compactly ?
# that problem goes away with Balrog due to the many -> latest mapping
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, buildTarget, buildID, comment) VALUES (1, 50, 'Firefox-3.6.11-build3', 100, 'minor', 'Firefox', '3.6.11', 'Darwin_Universal-gcc3', '20100930123656','Firefox-3.6.11-build1 mac');

# testing NULL matching
#INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, channel) VALUES (1, 30, 'BigBitBucket', 10, 'major', 'Firefox', NULL, 'release');
