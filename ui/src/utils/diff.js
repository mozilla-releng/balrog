import { NEW_LINES_REGEX } from './constants';

export default (diffProperties, objectOne, objectTwo) => {
  const prevValues = [];
  const nextValues = [];
  const formatValue = (value) => {
    switch (typeof value) {
      case 'string': {
        return value.replace(NEW_LINES_REGEX, '');
      }

      case 'object': {
        return JSON.stringify(value, null, 2);
      }

      default: {
        return value;
      }
    }
  };

  diffProperties
    .sort()
    .map((prop) => {
      const prev = objectOne[prop];
      const next = objectTwo[prop];

      // biome-ignore lint/suspicious/noDoubleEquals: checks for both undefined or null
      if (prev == next) {
        return null;
      }

      return {
        prev: `${prop}: ${formatValue(prev)}`,
        next: `${prop}: ${formatValue(next)}`,
      };
    })
    .filter(Boolean)
    .forEach(({ prev, next }) => {
      prevValues.push(prev);
      nextValues.push(next);
    });

  return [prevValues.join('\n'), nextValues.join('\n')];
};
