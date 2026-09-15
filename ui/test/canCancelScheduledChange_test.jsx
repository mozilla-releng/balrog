import { canCancelScheduledChange } from '../src/utils/rules';

describe('canCancelScheduledChange', () => {
  test('true for a scheduled update on an existing rule', () => {
    const result = canCancelScheduledChange({
      rule_id: 5,
      scheduledChange: { change_type: 'update' },
    });

    expect(result).toBe(true);
  });

  test('true for a scheduled delete on an existing rule', () => {
    const result = canCancelScheduledChange({
      rule_id: 5,
      scheduledChange: { change_type: 'delete' },
    });

    expect(result).toBe(true);
  });

  test('false for a scheduled insert (no rule exists yet)', () => {
    const result = canCancelScheduledChange({
      scheduledChange: { change_type: 'insert' },
    });

    expect(result).toBe(false);
  });

  test('false for a rule with no scheduled change', () => {
    const result = canCancelScheduledChange({
      rule_id: 5,
      scheduledChange: null,
    });

    expect(result).toBe(false);
  });
});
