import { title } from 'change-case';

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
        prev: `${title(prop)}: ${prev}`,
        next: `${title(prop)}: ${next}`,
      };
    })
    .filter(Boolean)
    .forEach(({ prev, next }) => {
      prevValues.push(prev);
      nextValues.push(next);
    });

  return [prevValues.join('\n'), nextValues.join('\n')];
};
