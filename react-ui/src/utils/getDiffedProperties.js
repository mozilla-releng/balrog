// This utility performs a diff and returns the list of properties
// where their values differ.
export default (diffProperties, objectOne, objectTwo) =>
  diffProperties.filter(prop => {
    const prev = objectOne[prop];
    const next = objectTwo[prop];

    // == checks for both undefined or null
    // eslint-disable-next-line eqeqeq
    if (prev == next) {
      return false;
    }

    return true;
  });
