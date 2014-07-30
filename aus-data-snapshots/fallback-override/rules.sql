# This tests that we can override a fallback channel properly. To make sure
# this is testable we send the fallback channel "release" to 5.0, and
# the full channel to 5.0.1. Thus, if the full channel gets sent to 5.0
# or to nothing at all, we know that's a FAIL.
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, channel) VALUES (1, 100, 'Firefox-5.0.1-build1', 100, 'minor', 'Firefox', 'release-cck-yahoo');
INSERT INTO rules (data_version, priority, mapping, backgroundRate, update_type, product, channel) VALUES (1, 100, 'Firefox-5.0-build1', 100, 'minor', 'Firefox', 'release');
