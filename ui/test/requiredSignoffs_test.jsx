import { getRequiredSignoffsForRule } from '../src/utils/requiredSignoffs';

const requiredSignoffs = [
  {
    product: 'Widevine',
    channel: 'release',
    role: 'releng',
    signoffs_required: 1,
  },
  {
    product: 'Widevine',
    channel: 'release',
    role: 'relman',
    signoffs_required: 1,
  },
  {
    product: 'Widevine',
    channel: 'release-localtest',
    role: 'releng',
    signoffs_required: 1,
  },
  {
    product: 'Widevine',
    channel: 'release-localtest',
    role: 'relman',
    signoffs_required: 1,
  },
  {
    product: 'Widevine',
    channel: 'release-cdntest',
    role: 'releng',
    signoffs_required: 1,
  },
  {
    product: 'Widevine',
    channel: 'release-cdntest',
    role: 'relman',
    signoffs_required: 1,
  },
  {
    product: 'Firefox',
    channel: 'release',
    role: 'releng',
    signoffs_required: 2,
  },
];

describe('getRequiredSignoffsForRule', () => {
  test('should require one of each role when several matching entries require one', () => {
    const result = getRequiredSignoffsForRule(
      { product: 'Widevine', channel: null },
      requiredSignoffs,
    );

    expect(result).toEqual({ releng: 1, relman: 1 });
  });

  test('should use the largest number of signoffs for each role', () => {
    const result = getRequiredSignoffsForRule({ product: 'Widevine' }, [
      ...requiredSignoffs,
      {
        product: 'Widevine',
        channel: 'beta',
        role: 'relman',
        signoffs_required: 2,
      },
    ]);

    expect(result).toEqual({ releng: 1, relman: 2 });
  });

  test('should only include required signoffs matching the channel', () => {
    const result = getRequiredSignoffsForRule(
      { product: 'Firefox', channel: 'release' },
      requiredSignoffs,
    );

    expect(result).toEqual({ releng: 2 });
  });

  test('should return an empty object when nothing matches', () => {
    const result = getRequiredSignoffsForRule(
      { product: 'Thunderbird', channel: 'release' },
      requiredSignoffs,
    );

    expect(result).toEqual({});
  });
});
