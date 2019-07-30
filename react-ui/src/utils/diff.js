import { title } from 'change-case';
import { NEW_LINES_REGEX } from './constants';

export default (diffProperties, objectOne, objectTwo) => {
  const prevValues = [];
  const nextValues = [];

  diffProperties
    .map(prop => {
      const prev = objectOne[prop];
      const next = objectTwo[prop];

      // == checks for both undefined or null
      // eslint-disable-next-line eqeqeq
      if (prev == next) {
        return null;
      }

      return {
        prev: `${title(prop)}: ${
          typeof prev === 'string' ? prev.replace(NEW_LINES_REGEX, '') : prev
        }`,
        next: `${title(prop)}: ${
          typeof next === 'string' ? next.replace(NEW_LINES_REGEX, '') : next
        }`,
      };
    })
    .filter(Boolean)
    .forEach(({ prev, next }) => {
      prevValues.push(prev);
      nextValues.push(next);
    });

  return [prevValues.join('\n'), nextValues.join('\n')];
};
