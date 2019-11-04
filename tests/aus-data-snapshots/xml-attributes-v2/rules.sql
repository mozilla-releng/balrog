# Simple 13.0 -> 13.0.1, multiple channels to test ftp and bouncer style urls
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, channel) VALUES (1, 100, 'Firefox-13.0.1-build1', 100, 'minor', 'Firefox', 'release');
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, channel) VALUES (1, 100, 'Firefox-13.0.1-build1', 100, 'minor', 'Firefox', 'betatest');
