import { ruleMatchesChannel } from '../src/utils/rules';

describe('channel matching', () => {
  test('should match when only current rule matches', () => {
    const result = ruleMatchesChannel(
      {
          channel: "nightly",
          scheduledChange: null,
        },
        "nightly",
    );
      expect(result).toBeTruthy();
  });
  test('should match when only scheduled change matches', () => {
    const result = ruleMatchesChannel(
      {
          channel: "nightly",
          scheduledChange: {
              "channel": "release",
          }
        },
        "release",
    );
      expect(result).toBeTruthy();
  });
  test('should match when rule is null', () => {
    const result = ruleMatchesChannel(
      {
          channel: null,
          scheduledChange: {
              channel: "nightly"
          },
        },
        "nightly",
    );
      expect(result).toBeTruthy();
  });
  test('should match when rule has glob', () => {
    const rule = {
          channel: "nightly*",
          scheduledChange: null,
        };
    const channels = ["nightly", "nightly-cdntest", "nightlytest"]
    const results = channels.map(c => ruleMatchesChannel(rule, c));
    expect(results).toEqual(expect.not.arrayContaining([false]));
  });
  test('should match when scheduled change has glob', () => {
      const rule = {
          channel: "nightly",
          scheduledChange: {
              "channel": "beta*",
          },
      };
          const channels = ["beta", "beta-localtest"];
    const results = channels.map(c => ruleMatchesChannel(rule, c));
    expect(results).toEqual(expect.not.arrayContaining([false]));
  });
  test('should match when rule and scheduled change have null channel', () => {
    const result = ruleMatchesChannel(
      {
          channel: null,
          scheduledChange: {
              channel: null,
          },
        },
        "nightly",
    );
      expect(result).toBeTruthy();
  });
  test('should not match rule substring without a glob', () => {
    const result = ruleMatchesChannel(
      {
          channel: "nightly",
          scheduledChange: null,
        },
        "nightly-cdntest",
    );
      expect(result).toBeFalsy();
  });
  test('should not match scheduled change substring without a glob', () => {
    const result = ruleMatchesChannel(
      {
          channel: "nightly",
          scheduledChange: {
            "channel": "beta",
          },
        },
        "beta-cdntest",
    );
      expect(result).toBeFalsy();
  });
  test('should not match when rule and scheduled change are a different channel', () => {
    const result = ruleMatchesChannel(
      {
          channel: "nightly",
          scheduledChange: {
              "channel": "beta",
          },
        },
        "release",
    );
      expect(result).toBeFalsy();
  });
});