import { tokenize, markEdits } from 'react-diff-view';

export default hunks => {
  if (!hunks) {
    return undefined;
  }

  const options = {
    highlight: false,
    enhancers: [markEdits(hunks, { type: 'line' })],
  };

  try {
    return tokenize(hunks, options);
  } catch (ex) {
    return undefined;
  }
};
