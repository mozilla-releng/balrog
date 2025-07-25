import { markEdits, tokenize } from 'react-diff-view';

export default (hunks) => {
  if (!hunks) {
    return undefined;
  }

  const options = {
    highlight: false,
    enhancers: [markEdits(hunks, { type: 'line' })],
  };

  try {
    return tokenize(hunks, options);
  } catch (_ex) {
    return undefined;
  }
};
