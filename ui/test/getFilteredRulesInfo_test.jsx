import getFilteredRulesInfo from '../src/utils/getFilteredRulesInfo';

describe('info for filtered rules', () => {
  let infoStartStr;

  beforeAll(() => {
    infoStartStr = 'No rules found';
  });

  test('should have rewind date when there is a rewind date and no product channel queries', () => {
    const date = new Date('2022-12-17T11:43:00');
    const result = getFilteredRulesInfo(null, date);

    expect(result).toMatch(`${infoStartStr} on ${date}.`);
  });
  test('should have rewind date and product when there is a rewind date and product query but no channel query', () => {
    const productChannelQueries = ['Firefox'];
    const date = new Date('2022-12-17T11:43:00');
    const result = getFilteredRulesInfo(productChannelQueries, date);

    expect(result).toMatch(
      `${infoStartStr} for the ${productChannelQueries[0]} channel on ${date}.`
    );
  });
  test('should have rewind date, product and channel when there is a rewind date, product query and channel query', () => {
    const productChannelQueries = ['Firefox', 'beta'];
    const date = new Date('2022-12-17T11:43:00');
    const result = getFilteredRulesInfo(productChannelQueries, date);

    expect(result).toMatch(
      `${infoStartStr} for the ${productChannelQueries[0]} ${productChannelQueries[1]} channel on ${date}.`
    );
  });
  test('should have scheduled changes string when scheduled changes filter is applied and there are no product channel queries', () => {
    const scheduledChangesStr = 'with scheduled changes.';
    const result = getFilteredRulesInfo(null, null, 1);

    expect(result).toMatch(`${infoStartStr} ${scheduledChangesStr}`);
  });
  test('should have scheduled changes string and product query when scheduled changes filter is applied and there product query but no channel query', () => {
    const productChannelQueries = ['Thunderbird'];
    const scheduledChangesStr = 'with scheduled changes.';
    const result = getFilteredRulesInfo(productChannelQueries, null, 1);

    expect(result).toMatch(
      `${infoStartStr} for the ${productChannelQueries[0]} channel ${scheduledChangesStr}`
    );
  });
  test('should have scheduled changes string, product query and channel query when scheduled changes filter is applied and there is a product query and channel query', () => {
    const productChannelQueries = ['Thunderbird', 'nightly'];
    const scheduledChangesStr = 'with scheduled changes.';
    const result = getFilteredRulesInfo(productChannelQueries, null, 1);

    expect(result).toMatch(
      `${infoStartStr} for the ${productChannelQueries[0]} ${productChannelQueries[1]} channel ${scheduledChangesStr}`
    );
  });
});
