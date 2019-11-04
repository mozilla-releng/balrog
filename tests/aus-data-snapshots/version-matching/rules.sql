# using priority to make matching order explicit
# < match for 3.6.7
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, channel) VALUES (1, 50, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '<3.6.8', 'release');
# <= match for 3.6.8
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, channel) VALUES (1, 40, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '<=3.6.8', 'release');
# >= for 3.6.11
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, channel) VALUES (1, 30, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '>=3.6.11', 'release');
# > for 3.6.10
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, channel) VALUES (1, 20, 'Firefox-3.6.12-build1', 100, 'minor', 'Firefox', '>3.6.9', 'release');
