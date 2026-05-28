import {
  buildProductChannelOptions,
  ruleMatchesChannel,
} from '../src/utils/rules';

describe('channel matching', () => {
  test('should match when only current rule matches', () => {
    const result = ruleMatchesChannel(
      {
        channel: 'nightly',
        scheduledChange: null,
      },
      'nightly',
    );

    expect(result).toBeTruthy();
  });
  test('should match when only scheduled change matches', () => {
    const result = ruleMatchesChannel(
      {
        channel: 'nightly',
        scheduledChange: {
          channel: 'release',
        },
      },
      'release',
    );

    expect(result).toBeTruthy();
  });
  test('should match when rule is null and scheduled change matches', () => {
    const result = ruleMatchesChannel(
      {
        scheduledChange: {
          channel: 'nightly',
        },
      },
      'nightly',
    );

    expect(result).toBeTruthy();
  });
  test('should match when rule has glob', () => {
    const rule = {
      channel: 'nightly*',
      scheduledChange: null,
    };
    const channels = ['nightly', 'nightly-cdntest', 'nightlytest'];
    const results = channels.map((c) => ruleMatchesChannel(rule, c));

    expect(results).toEqual(expect.not.arrayContaining([false]));
  });
  test('should match when scheduled change has glob', () => {
    const rule = {
      channel: 'nightly',
      scheduledChange: {
        channel: 'beta*',
      },
    };
    const channels = ['beta', 'beta-localtest'];
    const results = channels.map((c) => ruleMatchesChannel(rule, c));

    expect(results).toEqual(expect.not.arrayContaining([false]));
  });
  test('should match when rule is null and scheduled change has null channel', () => {
    const result = ruleMatchesChannel(
      {
        scheduledChange: {
          channel: null,
        },
      },
      'nightly',
    );

    expect(result).toBeTruthy();
  });
  test('should match when rule and scheduled change have null channel', () => {
    const result = ruleMatchesChannel(
      {
        channel: null,
        scheduledChange: {
          channel: null,
        },
      },
      'nightly',
    );

    expect(result).toBeTruthy();
  });
  test('should not match anything when rule is null and scheduled change is a different channel', () => {
    const result = ruleMatchesChannel(
      {
        scheduledChange: {
          channel: 'nightly',
        },
      },
      'beta',
    );

    expect(result).toBeFalsy();
  });
  test('should not match rule substring without a glob', () => {
    const result = ruleMatchesChannel(
      {
        channel: 'nightly',
        scheduledChange: null,
      },
      'nightly-cdntest',
    );

    expect(result).toBeFalsy();
  });
  test('should not match scheduled change substring without a glob', () => {
    const result = ruleMatchesChannel(
      {
        channel: 'nightly',
        scheduledChange: {
          channel: 'beta',
        },
      },
      'beta-cdntest',
    );

    expect(result).toBeFalsy();
  });
  test('should not match when rule and scheduled change are a different channel', () => {
    const result = ruleMatchesChannel(
      {
        channel: 'nightly',
        scheduledChange: {
          channel: 'beta',
        },
      },
      'release',
    );

    expect(result).toBeFalsy();
  });
  test('should not match when rule has a different channel and scheduled change type is delete with channel null', () => {
    const result = ruleMatchesChannel(
      {
        channel: 'aurora',
        scheduledChange: {
          change_type: 'delete',
          channel: null,
        },
      },
      'release',
    );

    expect(result).toBeFalsy();
  });
});

describe('buildProductChannelOptions', () => {
  const SEP = ' : ';

  test('includes product with no channel entry', () => {
    const options = buildProductChannelOptions(['Firefox'], [], [], SEP);

    expect(options).toEqual(['Firefox']);
  });

  test('includes exact channel when rule exists', () => {
    const rules = [{ product: 'Firefox', channel: 'nightly' }];
    const options = buildProductChannelOptions(
      ['Firefox'],
      ['nightly'],
      rules,
      SEP,
    );

    expect(options).toContain('Firefox : nightly');
  });

  test('strips * from wildcard channel', () => {
    const rules = [{ product: 'Firefox', channel: 'nightly*' }];
    const options = buildProductChannelOptions(
      ['Firefox'],
      ['nightly*'],
      rules,
      SEP,
    );

    expect(options).toContain('Firefox : nightly');
    expect(options).not.toContain('Firefox : nightly*');
  });

  test('deduplicates when both nightly and nightly* rules exist', () => {
    const rules = [
      { product: 'Firefox', channel: 'nightly' },
      { product: 'Firefox', channel: 'nightly*' },
    ];
    const options = buildProductChannelOptions(
      ['Firefox'],
      ['nightly', 'nightly*'],
      rules,
      SEP,
    );

    expect(options.filter((o) => o === 'Firefox : nightly')).toHaveLength(1);
  });

  test('does not add channel entry when no matching rule exists', () => {
    const rules = [{ product: 'Thunderbird', channel: 'nightly' }];
    const options = buildProductChannelOptions(
      ['Firefox'],
      ['nightly'],
      rules,
      SEP,
    );

    expect(options).not.toContain('Firefox : nightly');
  });

  test('handles multiple products and channels', () => {
    const rules = [
      { product: 'Firefox', channel: 'nightly*' },
      { product: 'Firefox', channel: 'release' },
      { product: 'Thunderbird', channel: 'beta*' },
    ];
    const options = buildProductChannelOptions(
      ['Firefox', 'Thunderbird'],
      ['nightly*', 'release', 'beta*'],
      rules,
      SEP,
    );

    expect(options).toContain('Firefox : nightly');
    expect(options).toContain('Firefox : release');
    expect(options).toContain('Thunderbird : beta');
    expect(options).not.toContain('Thunderbird : nightly');
    expect(options).not.toContain('Firefox : beta');
  });
});
