# Simple 5.0 -> 5.0.1, multiple channels to test ftp and bouncer style urls
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, channel) VALUES (1, 100, 'Firefox-5.0.1-build1', 100, 'minor', 'Firefox', '5.0*', 'release');
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, version, channel) VALUES (1, 100, 'Firefox-5.0.1-build1', 100, 'minor', 'Firefox', '5.0*', 'betatest');
